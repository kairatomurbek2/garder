from .base_views import BaseView, BaseTemplateView, BaseFormView
from django.http import Http404, JsonResponse
from django.core.urlresolvers import reverse
from webapp import filters, models, forms, perm_checkers
from django.views.generic import CreateView, UpdateView
from main.parameters import BP_TYPE, Messages, Groups
import paypalrestsdk
from paypalrestsdk.exceptions import ConnectionError
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ungettext as __
from webapp.exceptions import PaymentWasNotCreatedError
from django.conf import settings


class TestListView(BaseTemplateView):
    template_name = 'test/test_list.html'
    permission = "webapp.browse_test"

    def get_context_data(self, **kwargs):
        context = super(TestListView, self).get_context_data(**kwargs)
        tests = self._get_test_list()
        context['test_filter'] = filters.TestFilter(self.request.GET, queryset=tests)
        return context

    def _get_test_list(self):
        user = self.request.user
        paid_tests = models.Test.objects.filter(paid=True)
        if user.has_perm('webapp.access_to_all_tests'):
            return paid_tests
        if user.has_perm("webapp.access_to_pws_tests"):
            return paid_tests.filter(bp_device__site__pws__in=user.employee.pws.all())
        if user.has_perm('webapp.access_to_own_tests'):
            return paid_tests.filter(tester=user)


class TestDetailView(BaseTemplateView):
    permission = 'webapp.browse_test'
    template_name = 'test/test_detail.html'

    def get_context_data(self, **kwargs):
        context = super(TestDetailView, self).get_context_data(**kwargs)
        test = models.Test.objects.get(pk=self.kwargs['pk'])
        if not perm_checkers.TestPermChecker.has_perm(self.request, test):
            raise Http404
        if self.request.user != test.user and not test.paid:
            raise Http404
        context['test'] = test
        context['hazard'] = test.bp_device
        context['BP_TYPE'] = BP_TYPE
        return context


class UnpaidTestMixin(object):
    def get_unpaid_tests(self):
        user = self.request.user
        unpaid_tests = models.Test.objects.filter(paid=False)
        if user.has_perm('webapp.access_to_all_tests'):
            return unpaid_tests
        if user.has_perm("webapp.access_to_pws_tests"):
            groups = models.Group.objects.filter(name__in=[Groups.admin, Groups.pws_owner])
            users = models.User.objects.filter(employee__pws=user.employee.pws.all(), groups=groups)
            return unpaid_tests.filter(user__in=users)
        if user.has_perm('webapp.access_to_own_tests'):
            return unpaid_tests.filter(user=user)


class UnpaidTestView(BaseTemplateView, UnpaidTestMixin):
    template_name = 'test/unpaid_test_list.html'
    permission = 'webapp.browse_test'

    def get_context_data(self, **kwargs):
        context = super(UnpaidTestView, self).get_context_data(**kwargs)
        tests = self.get_unpaid_tests()
        context['test_filter'] = filters.TestFilter(self.request.GET, queryset=tests)
        context['payment_form'] = forms.PaymentForm(queryset=tests)
        return context


class TestPayPaypalView(BaseView, UnpaidTestMixin):
    SUCCESS = 'success'
    CANCEL = 'cancel'

    def get(self, request, *args, **kwargs):
        action = self.request.GET['action']
        if action == self.SUCCESS:
            payment_id = self.request.GET['paymentId']
            payer_id = self.request.GET['PayerID']
            payment = paypalrestsdk.Payment.find(payment_id)
            if payment.execute({'payer_id': payer_id}):
                test_pks = self.request.GET['tests'].split(',')
                models.Test.objects.filter(pk__in=test_pks).update(paid=True, paypal_payment_id=payment_id)
                messages.success(self.request, __(Messages.Test.payment_successful_singular, Messages.Test.payment_successful_plural, len(test_pks)))
            else:
                messages.error(self.request, Messages.Test.payment_failed)
        else:
            messages.error(self.request, Messages.Test.payment_cancelled)
        return redirect('webapp:unpaid_test_list')

    def post(self, request, *args, **kwargs):
        payment_form = forms.PaymentForm(self.request.POST, queryset=self.get_unpaid_tests())
        if payment_form.is_valid():
            payment = self.get_payment(payment_form.cleaned_data['tests'])
            try:
                if payment.create():
                    # we need to find approval_url and redirect user to this url
                    for link in payment.links:
                        if link['rel'] == 'approval_url':
                            approval_url = link['href']
                    response = {'status': 'success', 'approval_url': approval_url,
                                'total_amount': payment.transactions[0]['amount']['total']}
                else:
                    raise PaymentWasNotCreatedError(payment.error)
            except (ConnectionError, PaymentWasNotCreatedError, NameError):
                response = {'status': 'error', 'message': Messages.Test.payment_failed}
        else:
            response = payment_form.errors
        return JsonResponse(response)

    def get_payment(self, tests):
        total_amount = sum((test.price for test in tests))
        items = [
            {
                "quantity": 1,
                "name": "Payment for test #%s" % test.pk,
                "price": "%.2f" % test.price,
                "currency": "USD"
            }
            for test in tests
            ]

        test_pks = ','.join((str(test.pk) for test in tests))

        return paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": "%s%s?action=%s&tests=%s" % (
                    settings.HOST, reverse('webapp:test_pay_paypal'), self.SUCCESS, test_pks),
                "cancel_url": "%s%s?action=%s&tests=%s" % (
                    settings.HOST, reverse('webapp:test_pay_paypal'), self.CANCEL, test_pks)
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
                    "description": "Payment for tests"
                }
            ]
        })


class TestBaseFormView(BaseFormView):
    template_name = 'test/test_form.html'
    form_class = forms.TestForm
    model = models.Test
    hazard = None

    def get_context_data(self, **kwargs):
        context = super(TestBaseFormView, self).get_context_data(**kwargs)
        context['BP_TYPE'] = BP_TYPE
        context['hazard'] = self.get_hazard()
        return context

    def get_success_url(self):
        return reverse('webapp:test_detail', args=(self.object.pk,))

    def get_form(self, form_class):
        form = super(TestBaseFormView, self).get_form(form_class)
        form.fields['tester'].queryset = self._get_queryset_for_tester_field()
        form.bp_type = self.get_hazard().bp_type_required
        return form

    def _get_queryset_for_tester_field(self):
        queryset = models.User.objects.none()
        user = self.request.user
        if self.request.user.has_perm('webapp.access_to_own_tests'):
            queryset = models.User.objects.filter(pk=user.pk)
        if self.request.user.has_perm('webapp.access_to_pws_tests'):
            queryset = models.User.objects.filter(groups__name__in=[Groups.tester, Groups.admin, Groups.pws_owner],
                                                  employee__pws__in=user.employee.pws.all()).distinct()
        if self.request.user.has_perm('webapp.access_to_all_tests'):
            queryset = models.User.objects.filter(
                groups__name__in=[Groups.tester, Groups.admin, Groups.pws_owner]
            ).distinct()
        return queryset


class TestAddView(TestBaseFormView, CreateView):
    permission = 'webapp.add_test'
    success_message = Messages.Test.adding_success
    error_message = Messages.Test.adding_error

    def get_hazard(self):
        if self.hazard:
            return self.hazard
        self.hazard = models.Hazard.objects.get(pk=self.kwargs['pk'])
        return self.hazard

    def get_form(self, form_class):
        if not perm_checkers.HazardPermChecker.has_perm(self.request, models.Hazard.objects.get(pk=self.kwargs['pk'])):
            raise Http404
        return super(TestAddView, self).get_form(form_class)

    def get_success_url(self):
        return reverse('webapp:test_edit', args=(self.object.pk,))

    def form_valid(self, form):
        form.instance.bp_device = models.Hazard.objects.get(pk=self.kwargs['pk'])
        form.instance.user = self.request.user
        response = super(TestAddView, self).form_valid(form)
        self.request.session['test_for_payment_pk'] = self.object.pk
        return response


class TestEditView(TestBaseFormView, UpdateView):
    permission = 'webapp.change_test'
    success_message = Messages.Test.editing_success
    error_message = Messages.Test.editing_error

    def get_hazard(self):
        if self.hazard:
            return self.hazard
        self.hazard = models.Test.objects.get(pk=self.kwargs['pk']).bp_device
        return self.hazard

    def get_context_data(self, **kwargs):
        context = super(TestEditView, self).get_context_data(**kwargs)
        context['test_for_payment_pk'] = self.request.session.pop('test_for_payment_pk', None)
        return context

    def get_form(self, form_class):
        form = super(TestEditView, self).get_form(form_class)
        if not perm_checkers.TestPermChecker.has_perm(self.request, form.instance):
            raise Http404
        if form.instance.user != self.request.user and not form.instance.paid:
            raise Http404
        return form

    def get_initial(self):
        initial = {}
        if not self.object.air_inlet_opened:
            initial['air_inlet_did_not_open'] = True
        if not self.object.rv_opened:
            initial['rv_did_not_open'] = True
        return initial