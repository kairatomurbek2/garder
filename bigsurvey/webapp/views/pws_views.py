from decimal import Decimal
from django.conf import settings
from .base_views import BaseTemplateView, BaseFormView, BaseView
from django.contrib import messages
from django.http import Http404, JsonResponse
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
import paypalrestsdk
from webapp import models, forms
from main.parameters import Messages, BP_TYPE, LetterTypes, BPLocations, Groups, DEMO_TRIAL_PRICE
from django.views.generic import UpdateView, CreateView
from django.utils.translation import ugettext as _
from datetime import date
from webapp.actions.demo_trial import PayAndActivate
from webapp.exceptions import PaymentWasNotCreatedError, PaymentTotalSumIsNull


class PWSListView(BaseTemplateView):
    template_name = 'pws/pws_list.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(PWSListView, self).get_context_data(**kwargs)
        if user.has_perm('webapp.browse_all_pws'):
            pws_list = models.PWS.active_only.all().order_by('-pk')
        elif user.has_perm('webapp.own_multiple_pws'):
            if user.groups.filter(name=Groups.ad_auth):
                pws_list = user.employee.pws.filter(is_active=True).order_by('-pk')
            else:
                pws_list = user.employee.pws.all().order_by('-pk')
        else:
            raise Http404
        context['pws_list'] = pws_list
        return context


class PWSDetailView(BaseTemplateView):
    template_name = 'pws/pws.html'
    permission = 'webapp.browse_pws'

    def get_context_data(self, **kwargs):
        context = super(PWSDetailView, self).get_context_data(**kwargs)
        pws = models.PWS.active_only.get(pk=self.kwargs['pk'])
        user = self.request.user
        if not user.is_superuser and user.has_perm('webapp.change_own_pws') and pws not in user.employee.pws.all():
            raise Http404
        context['pws'] = pws
        return context


class PWSBaseFormView(BaseFormView):
    template_name = 'pws/pws_form.html'
    form_class = forms.PWSForm
    model = models.PWS

    def get_success_url(self):
        return reverse('webapp:pws_detail', args=(self.object.pk,))


class PWSAddView(PWSBaseFormView, CreateView):
    permission = 'webapp.add_pws'
    success_message = Messages.PWS.adding_success
    error_message = Messages.PWS.adding_error

    def form_valid(self, form):
        form_is_valid = super(PWSAddView, self).form_valid(form)
        self.object.is_active = True
        self.object.save()
        user = self.request.user
        if user.has_perm('webapp.own_multiple_pws'):
            user.employee.pws.add(self.object)
            user.employee.save()
        return form_is_valid


class PWSEditView(PWSBaseFormView, UpdateView):
    permission = 'webapp.change_pws'
    success_message = Messages.PWS.editing_success
    error_message = Messages.PWS.editing_error
    form_class_for_admin = forms.PWSFormForAdmin

    def get_form_class(self):
        user = self.request.user
        if not user.is_superuser and user.has_perm('webapp.change_own_pws'):
            return self.form_class_for_admin
        return self.form_class

    def get_context_data(self, **kwargs):
        user = self.request.user
        if not user.is_superuser and user.has_perm('webapp.change_own_pws') and self.object not in user.employee.pws.all():
            raise Http404
        return super(PWSEditView, self).get_context_data(**kwargs)


class SnapshotItem(object):
    def __init__(self, title='', value=None):
        self.title = title
        self.value = value


class SnapshotView(BaseTemplateView):
    template_name = 'pws/snapshot.html'
    permission = 'webapp.browse_pws'
    pws = None

    def get_context_data(self, **kwargs):
        self.pws = models.PWS.objects.get(pk=self.kwargs['pk'])
        if self._allowed():
            context = super(SnapshotView, self).get_context_data(**kwargs)
            context['snapshot_items'] = self._get_snapshot_items()
            context['pws_pk'] = self.pws.pk
            return context
        raise Http404

    def _allowed(self):
        return self.request.user.is_superuser or self.pws in self.request.user.employee.pws.all()

    def _get_snapshot_items(self):
        snapshot_items = [
            SnapshotItem(_('Surveys Performed'), self._get_surveys_performed()),
            SnapshotItem(_('Due Install 1st letters Sent'),
                         self._get_letters_sent(letter_type=LetterTypes.DUE_INSTALL_FIRST)),
            SnapshotItem(_('Due Install 2nd letters Sent'),
                         self._get_letters_sent(letter_type=LetterTypes.DUE_INSTALL_SECOND)),
            SnapshotItem(_('Due Install 3rd letters Sent'),
                         self._get_letters_sent(letter_type=LetterTypes.DUE_INSTALL_THIRD)),
            SnapshotItem(_('Annual Test 1st letters Sent'),
                         self._get_letters_sent(letter_type=LetterTypes.ANNUAL_TEST_FIRST)),
            SnapshotItem(_('Annual Test 2nd letters Sent'),
                         self._get_letters_sent(letter_type=LetterTypes.ANNUAL_TEST_SECOND)),
            SnapshotItem(_('Annual Test 3rd letters Sent'),
                         self._get_letters_sent(letter_type=LetterTypes.ANNUAL_TEST_THIRD)),
            SnapshotItem(_('No. of Containment Assemblies'),
                         self._get_bp_devices(bp_location=BPLocations.AT_METER)),
            SnapshotItem(_('No. of Isolation Assemblies'),
                         self._get_bp_devices(bp_location=BPLocations.INTERNAL)),
            SnapshotItem(_('No. of RP Backflow Preventers'),
                         self._get_bp_devices(bp_type_group=BP_TYPE.RP_TYPES)),
            SnapshotItem(_('No. of DC Backflow Preventers'),
                         self._get_bp_devices(bp_type_group=BP_TYPE.DC_TYPES)),
            SnapshotItem(_('No. of PVB Backflow Preventers'),
                         self._get_bp_devices(bp_type_group=BP_TYPE.STANDALONE_TYPES)),
        ]
        return snapshot_items

    def _get_surveys_performed(self, from_date=None, to_date=None):
        if not from_date:
            from_date = date(year=1900, month=1, day=1)
        if not to_date:
            to_date = date(year=3000, month=12, day=31)
        return models.Survey.objects.filter(
            site__pws=self.pws,
            survey_date__gt=from_date,
            survey_date__lt=to_date
        ).count()

    def _get_letters_sent(self, letter_type=None, from_date=None, to_date=None):
        if not from_date:
            from_date = date(year=1900, month=1, day=1)
        if not to_date:
            to_date = date(year=3000, month=12, day=31)
        return models.Letter.objects.filter(
            site__pws=self.pws,
            date__gt=from_date,
            date__lt=to_date,
            already_sent=True,
            letter_type__letter_type__icontains=letter_type
        ).count()

    def _get_bp_devices(self, bp_location=None, bp_type_group=None):
        filter_kwargs = {
            'hazard__site__pws': self.pws
        }
        if bp_location:
            filter_kwargs['assembly_location__assembly_location'] = bp_location
        if bp_type_group:
            filter_kwargs['bp_type_present__in'] = bp_type_group
        return models.BPDevice.objects.filter(**filter_kwargs).count()


class ActivateBlockedPWS(BaseTemplateView):
    template_name = 'pws/activate_blocked_pws.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(ActivateBlockedPWS, self).get_context_data(**kwargs)
        if not user.employee.has_paid and user.groups.filter(name=Groups.pws_owner).count():
            context['user'] = user
            context['can_pay'] = True
            return context
        context['can_pay'] = False
        return context


class DemoTrialPayPaypalView(BaseView):
    SUCCESS = 'success'
    CANCEL = 'cancel'

    def get(self, request, *args, **kwargs):
        action = self.request.GET['action']
        if action == self.SUCCESS:
            payment_id = self.request.GET['paymentId']
            payer_id = self.request.GET['PayerID']
            payment = paypalrestsdk.Payment.find(payment_id)
            if payment.execute({'payer_id': payer_id}):
                pws_list = self.request.user.employee.pws.all()
                for pws in pws_list:
                    PayAndActivate.pay_and_activate(pws, request)
                messages.success(self.request,
                                 (Messages.PWS.payment_successful_singular))
            else:
                messages.error(self.request, Messages.PWS.payment_failed)
        else:
            messages.error(self.request, Messages.PWS.payment_cancelled)
            return redirect('webapp:activate_blocked_pws')
        return redirect('webapp:home')

    def post(self, request, *args, **kwargs):
        price_obj = models.PriceHistory.objects.filter(price_type=DEMO_TRIAL_PRICE).order_by('start_date')[0]
        demo_trial_price = price_obj.price
        payment = self.get_payment(demo_trial_price)
        if payment.create():
            approval_url = self._get_approve_url(payment)
            response = {'status': 'success', 'approval_url': approval_url,
                        'total_amount': payment.transactions[0]['amount']['total']}
        else:
            raise PaymentWasNotCreatedError(payment.error)
        return JsonResponse(response)

    def _get_approve_url(self, payment):
        for link in payment.links:
            if link['rel'] == 'approval_url':
                approval_url = link['href']
        return approval_url

    def get_payment(self, demo_trial_price):
        total_amount = demo_trial_price
        if total_amount.compare(Decimal(0)) == 0:
            raise PaymentTotalSumIsNull()
        items = [
            {
                "quantity": 1,
                "name": "Payment for system usage",
                "price": "%.2f" % demo_trial_price,
                "currency": "USD"
            }
        ]

        return paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": "%s%s?action=%s" % (
                    settings.HOST, reverse('webapp:demo_trial_paypal'), self.SUCCESS),
                "cancel_url": "%s%s?action=%s" % (
                    settings.HOST, reverse('webapp:demo_trial_paypal'), self.CANCEL)
            },
            "transactions": [
                {
                    "item_list": {
                        "items": items
                    },
                    "amount": {
                        "total": "%.2f" % total_amount,
                        "currency": "USD"
                    },
                    "description": "Payment for demo trial"
                }
            ]
        })
