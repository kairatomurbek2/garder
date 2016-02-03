from .base_views import BaseTemplateView, BaseFormView
from django.http import Http404
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from webapp import models, forms
from main.parameters import Messages, BP_TYPE, LetterTypes, BPLocations
from django.views.generic import UpdateView, CreateView
from django.utils.translation import ugettext as _
from datetime import date
from webapp.actions.demo_trial import PayAndActivate


class PWSListView(BaseTemplateView):
    template_name = 'pws/pws_list.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(PWSListView, self).get_context_data(**kwargs)
        if user.has_perm('webapp.browse_all_pws'):
            pws_list = models.PWS.objects.all()
        elif user.has_perm('webapp.own_multiple_pws'):
            pws_list = user.employee.pws.all()
        else:
            raise Http404
        context['pws_list'] = pws_list
        return context


class PWSDetailView(BaseTemplateView):
    template_name = 'pws/pws.html'
    permission = 'webapp.browse_pws'

    def get_context_data(self, **kwargs):
        context = super(PWSDetailView, self).get_context_data(**kwargs)
        pws = models.PWS.objects.get(pk=self.kwargs['pk'])
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
        context['user'] = user
        return context

    def post(self, request, *args, **kwargs):
        pws_list = self.request.user.employee.pws.all()
        for pws in pws_list:
            PayAndActivate.pay_and_activate(pws, request)
        return redirect('webapp:home')
