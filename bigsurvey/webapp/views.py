from collections import OrderedDict
import json
from smtplib import SMTPException
import time
import os

from django.conf import settings

from django.core.files.storage import default_storage
from django.db import IntegrityError, connection
from django.db.models import NOT_PROVIDED
from django.forms import formset_factory, ModelChoiceField
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.generic import TemplateView, CreateView, UpdateView, FormView, View
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext as __
from django.core.mail import EmailMessage
import paypalrestsdk
from paypalrestsdk.exceptions import ConnectionError

from webapp import perm_checkers, models, forms, filters
from main.parameters import Messages, Groups, TESTER_ASSEMBLY_STATUSES, ADMIN_GROUPS, OTHER, DATEFORMAT_HELP
from webapp.exceptions import PaymentWasNotCreatedError
from webapp.raw_sql_queries import HazardPriorityQuery
from webapp.responses import PDFResponse
from webapp.utils.letter_renderer import LetterRenderer
from webapp.forms import TesterSiteSearchForm, ImportMappingsForm, BaseImportMappingsFormSet, ImportForm
from webapp.utils.pdf_generator import PDFGenerator
from webapp.utils import photo_util
from webapp.utils.excel_parser import ExcelParser, DateFormatError, FINISHED, BackgroundExcelParserRunner


class PermissionRequiredMixin(View):
    permission = None

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.permission and not self.request.user.has_perm(self.permission):
            raise Http404
        return super(PermissionRequiredMixin, self).dispatch(*args, **kwargs)


class BaseView(PermissionRequiredMixin):
    pass


class BaseTemplateView(BaseView, TemplateView):
    pass


class BaseFormView(BaseView, FormView):
    success_message = None
    error_message = None

    def form_valid(self, form):
        if self.success_message:
            messages.success(self.request, self.success_message)
        return super(BaseFormView, self).form_valid(form)

    def form_invalid(self, form):
        if self.error_message:
            messages.error(self.request, self.error_message)
        return super(BaseFormView, self).form_invalid(form)


class HomeView(BaseTemplateView):
    template_name = "home.html"
    permission = 'webapp.browse_site'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_superuser and user.has_perm('webapp.access_to_site_by_customer_account'):
            return redirect(reverse('webapp:tester-home'))
        return super(HomeView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(HomeView, self).get_context_data(**kwargs)
        sites = self._get_sites(user)
        context['site_filter'] = filters.SiteFilter(self.request.GET, queryset=sites)
        return context

    def _get_sites(self, user):
        if user.has_perm('webapp.access_to_all_sites'):
            return models.Site.objects.all()
        if user.has_perm('webapp.access_to_pws_sites'):
            return models.Site.objects.filter(pws=user.employee.pws)
        return []


class TesterHomeView(BaseTemplateView, FormView):
    template_name = 'tester_home.html'
    permission = 'webapp.access_to_site_by_customer_account'
    form_class = TesterSiteSearchForm

    def get_context_data(self, **kwargs):
        kwargs['form'] = self.form_class(self.request.POST or None)
        return super(TesterHomeView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.request.session['site_pk'] = form.site.pk
        return redirect(reverse('webapp:site_detail', args=(form.site.pk,)))


class SiteDetailView(BaseTemplateView):
    template_name = 'site/site.html'
    permission = 'webapp.browse_site'

    def get_context_data(self, **kwargs):
        site = models.Site.objects.get(pk=self.kwargs['pk'])
        if not perm_checkers.SitePermChecker.has_perm(self.request, site):
            raise Http404
        context = super(SiteDetailView, self).get_context_data(**kwargs)
        context['site'] = site
        return context


class SiteBaseFormView(BaseFormView):
    template_name = 'site/site_form.html'
    form_class = forms.SiteForm
    form_class_for_surveyor = forms.SiteFormForSurveyor
    model = models.Site

    def get_form_class(self):
        if self.request.user.has_perm('webapp.change_all_info_about_site'):
            return self.form_class
        return self.form_class_for_surveyor

    def get_form(self, form_class):
        form = super(SiteBaseFormView, self).get_form(form_class)
        if self.request.user.has_perm('webapp.change_all_info_about_site'):
            if not self.request.user.has_perm('webapp.access_to_all_sites'):
                form.fields['pws'].queryset = models.PWS.objects.filter(pk=self.request.user.employee.pws.pk)
        return form

    def get_success_url(self):
        return reverse('webapp:site_detail', args=(self.object.pk,))


class SiteAddView(SiteBaseFormView, CreateView):
    permission = 'webapp.add_site'
    success_message = Messages.Site.adding_success
    error_message = Messages.Site.adding_error


class SiteEditView(SiteBaseFormView, UpdateView):
    permission = 'webapp.change_site'
    success_message = Messages.Site.editing_success
    error_message = Messages.Site.editing_error

    def get_form(self, form_class):
        form = super(SiteEditView, self).get_form(form_class)
        if not perm_checkers.SitePermChecker.has_perm(self.request, form.instance):
            raise Http404
        return form


class BatchUpdateView(BaseTemplateView):
    template_name = 'site/site_batch_update.html'
    permission = 'webapp.access_to_batch_update'
    filter_class = filters.SiteFilter
    form_class = forms.BatchUpdateForm

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(BatchUpdateView, self).get_context_data(**kwargs)
        sites = self._get_sites(user)
        context['site_filter'] = self._get_site_filter(queryset=sites)
        context['form'] = self.form_class()
        return context

    @staticmethod
    def _get_sites(user):
        sites = []
        if user.has_perm('webapp.access_to_pws_sites'):
            sites = models.Site.objects.filter(pws=user.employee.pws)
        if user.has_perm('webapp.access_to_all_sites'):
            sites = models.Site.objects.all()
        return sites

    def _get_site_filter(self, queryset):
        return self.filter_class(self.request.GET, queryset=queryset)

    def post(self, request):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            date = form.cleaned_data.get('date')
            site_pks = self.request.POST.getlist('site_pks')
            self._batch_update(date, site_pks)
            messages.success(self.request, Messages.BatchUpdate.success)
        else:
            messages.error(self.request, Messages.BatchUpdate.error)
        return redirect(self.get_success_url())

    def _batch_update(self, date, site_pks):
        if 'set_sites_next_survey_date' in self.request.POST:
            self._batch_update_sites(date, site_pks)
        else:
            self._batch_update_hazards(date, site_pks)

    def _batch_update_sites(self, date, site_pks):
        models.Site.objects.filter(pk__in=site_pks).update(next_survey_date=date)

    def _batch_update_hazards(self, date, site_pks):
        for site_pk in site_pks:
            models.Site.objects.get(pk=site_pk).hazards.update(due_install_test_date=date)

    def get_success_url(self):
        return reverse('webapp:batch_update')


class PWSListView(BaseTemplateView):
    template_name = 'pws/pws_list.html'
    permission = 'webapp.browse_pws'

    def get_context_data(self, **kwargs):
        context = super(PWSListView, self).get_context_data(**kwargs)
        context['pws_list'] = models.PWS.objects.all()
        return context


class PWSBaseFormView(BaseFormView):
    template_name = 'pws/pws_form.html'
    form_class = forms.PWSForm
    model = models.PWS

    def get_success_url(self):
        return reverse('webapp:pws_list')


class PWSAddView(PWSBaseFormView, CreateView):
    permission = 'webapp.add_pws'
    success_message = Messages.PWS.adding_success
    error_message = Messages.PWS.adding_error


class PWSEditView(PWSBaseFormView, UpdateView):
    permission = 'webapp.change_pws'
    success_message = Messages.PWS.editing_success
    error_message = Messages.PWS.editing_error


class SurveyDetailView(BaseTemplateView):
    template_name = 'survey/survey.html'
    permission = 'webapp.browse_survey'

    def get_context_data(self, **kwargs):
        survey = models.Survey.objects.get(pk=self.kwargs['pk'])
        if not perm_checkers.SurveyPermChecker.has_perm(self.request, survey):
            raise Http404
        context = super(SurveyDetailView, self).get_context_data(**kwargs)
        context['survey'] = survey
        context['hazards'] = survey.hazards.all()
        context['service'] = survey.service_type.service_type
        return context


class SurveyBaseFormView(BaseFormView):
    template_name = 'survey/survey_form.html'
    form_class = forms.SurveyForm
    model = models.Survey

    def get_context_data(self, **kwargs):
        context = super(SurveyBaseFormView, self).get_context_data(**kwargs)
        context['hazard_form'] = forms.HazardForm()
        return context

    def get_form(self, form_class):
        form = super(SurveyBaseFormView, self).get_form(form_class)
        form.fields['surveyor'].queryset = self._get_queryset_for_surveyor_field()
        form.fields['hazards'].queryset = self._get_queryset_for_hazards_field(form.instance)
        return form

    def _get_queryset_for_hazards_field(self, survey):
        try:
            site = survey.site
            service_type = survey.service_type
        except AttributeError:
            site = models.Site.objects.get(pk=self.kwargs['pk'])
            service_type = models.ServiceType.objects.get(service_type=self.kwargs['service'])
        return site.hazards.filter(service_type=service_type)

    def _get_queryset_for_surveyor_field(self):
        queryset = []
        if self.request.user.has_perm('webapp.access_to_own_surveys'):
            queryset = models.User.objects.filter(pk=self.request.user.pk)
        if self.request.user.has_perm('webapp.access_to_pws_surveys'):
            queryset = models.User.objects.filter(
                groups__name=Groups.surveyor,
                employee__pws=self.request.user.employee.pws
            )
        if self.request.user.has_perm('webapp.access_to_all_surveys'):
            queryset = models.User.objects.filter(groups__name=Groups.surveyor)
        return queryset

    def get_success_url(self):
        return reverse('webapp:survey_detail', args=(self.object.pk,))


class SurveyAddView(SurveyBaseFormView, CreateView):
    permission = 'webapp.add_survey'
    success_message = Messages.Survey.adding_success
    error_message = Messages.Survey.adding_error

    def get_context_data(self, **kwargs):
        context = super(SurveyAddView, self).get_context_data(**kwargs)
        context['site_pk'] = self.kwargs['pk']
        context['service_type'] = self.kwargs['service']
        context['fire'] = self._is_fire_service()
        return context

    def _is_fire_service(self):
        if self.kwargs['service'] == 'fire':
            return True
        return False

    def form_valid(self, form):
        site = self._get_site()
        form.instance.site = site
        form.instance.service_type = self._get_service_type()
        response = super(SurveyAddView, self).form_valid(form)
        survey = site.surveys.latest('survey_date')
        site.last_survey_date = survey.survey_date
        if form.instance.service_type.service_type == 'potable':
            site.potable_present = True
        elif form.instance.service_type.service_type == 'fire':
            site.fire_present = True
        elif form.instance.service_type.service_type == 'irrigation':
            site.irrigation_present = True
        site.save()
        for hazard in site.hazards.all():
            if hazard in survey.hazards.all():
                hazard.is_present = True
            else:
                hazard.is_present = False
            hazard.save()
        return response

    def _get_site(self):
        site = models.Site.objects.get(pk=self.kwargs['pk'])
        if not perm_checkers.SitePermChecker.has_perm(self.request, site):
            raise Http404
        return site

    def _get_service_type(self):
        return models.ServiceType.objects.filter(service_type__icontains=self.kwargs['service'])[0]

    def get_form(self, form_class):
        if not perm_checkers.SitePermChecker.has_perm(self.request, self._get_site()):
            raise Http404
        return super(SurveyAddView, self).get_form(form_class)


class SurveyEditView(SurveyBaseFormView, UpdateView):
    permission = 'webapp.add_survey'
    success_message = Messages.Survey.editing_success
    error_message = Messages.Survey.editing_error

    def get_context_data(self, **kwargs):
        context = super(SurveyEditView, self).get_context_data(**kwargs)
        context['site_pk'] = self.object.site.pk
        context['service_type'] = self.object.service_type.service_type
        return context

    def get_form(self, form_class):
        form = super(SurveyEditView, self).get_form(form_class)
        if not perm_checkers.SurveyPermChecker.has_perm(self.request, form.instance):
            raise Http404
        return form

    def form_valid(self, form):
        site = form.instance.site
        super(SurveyEditView, self).form_valid(form)
        survey = site.surveys.latest('survey_date')
        site.last_survey_date = survey.survey_date
        site.save()
        for hazard in site.hazards.all():
            if hazard in survey.hazards.all():
                hazard.is_present = True
            else:
                hazard.is_present = False
            hazard.save()
        return HttpResponseRedirect(self.get_success_url())


class HazardDetailView(BaseTemplateView):
    template_name = 'hazard/hazard.html'
    permission = 'webapp.browse_hazard'

    def get_context_data(self, **kwargs):
        context = super(HazardDetailView, self).get_context_data(**kwargs)
        context['hazard'] = self._get_hazard()
        context['countlte0'] = self._is_tests_count_lte0(context['hazard'])
        return context

    def _get_hazard(self):
        hazard = models.Hazard.objects.get(pk=self.kwargs['pk'])
        if not perm_checkers.HazardPermChecker.has_perm(self.request, hazard):
            raise Http404
        return hazard

    def _is_tests_count_lte0(self, hazard):
        tests_count = models.Test.objects.filter(bp_device=hazard, tester=self.request.user, paid=True).count()
        return tests_count <= 0


class HazardBaseFormView(BaseFormView):
    template_name = 'hazard/hazard_form.html'
    form_class = forms.HazardForm
    form_class_for_tester = forms.HazardFormForTester
    model = models.Hazard

    def get_success_url(self):
        return reverse('webapp:hazard_detail', args=(self.object.pk,))

    def form_valid(self, form):
        self.object = form.save()
        if self.request.FILES.get('photo'):
            photo_thumb = photo_util.create_thumbnail(self.object.photo)
            self.object.photo_thumb.save(self.object.photo.name, photo_thumb)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.get_success_url())


class HazardAddView(HazardBaseFormView, CreateView):
    permission = 'webapp.add_hazard'
    success_message = Messages.Hazard.adding_success
    error_message = Messages.Hazard.adding_error

    AJAX_OK = 'ok'
    AJAX_ERROR = 'error'

    def get_context_data(self, **kwargs):
        context = super(HazardAddView, self).get_context_data(**kwargs)
        context['site_pk'] = self.kwargs['pk']
        context['service_type'] = self.kwargs['service']
        return context

    def ajax_response(self, status, form):
        json_data = {}
        context = self.get_context_data()
        if status == self.AJAX_OK:
            context['form'] = forms.HazardForm()
            json_data['option'] = {
                'value': self.object.pk,
                'text': str(self.object)
            }
        else:
            context['form'] = form
        json_data['status'] = status
        json_data['form'] = render_to_string('hazard/partial/hazard_form.html', context, RequestContext(self.request))
        return JsonResponse(json_data)

    def get_form(self, form_class):
        site = models.Site.objects.get(pk=self.kwargs['pk'])
        if not perm_checkers.SitePermChecker.has_perm(self.request, site):
            raise Http404
        return super(HazardAddView, self).get_form(form_class)

    def form_valid(self, form):
        form.instance.site = models.Site.objects.get(pk=self.kwargs['pk'])
        form.instance.service_type = models.ServiceType.objects.get(service_type=self.kwargs['service'])
        response = super(HazardAddView, self).form_valid(form)
        self._switch_on_service_type(form.instance.site, self.kwargs['service'])
        if self.request.is_ajax():
            return self.ajax_response(self.AJAX_OK, form)
        return response

    def _switch_on_service_type(self, site, service_type):
        if service_type == 'potable':
            site.potable_present = True
        elif service_type == 'fire':
            site.fire_present = True
        elif service_type == 'irrigation':
            site.irrigation_present = True
        site.save()

    def form_invalid(self, form):
        response = super(HazardAddView, self).form_invalid(form)
        if self.request.is_ajax():
            return self.ajax_response(self.AJAX_ERROR, form)
        return response


class HazardEditView(HazardBaseFormView, UpdateView):
    permission = 'webapp.change_hazard'
    success_message = Messages.Hazard.editing_success
    error_message = Messages.Hazard.editing_error

    def get_form_class(self):
        if self.request.user.has_perm('webapp.change_all_info_about_hazard'):
            return self.form_class
        else:
            return self.form_class_for_tester

    def get_form(self, form_class):
        form = super(HazardEditView, self).get_form(form_class)
        if not perm_checkers.HazardPermChecker.has_perm(self.request, form.instance):
            raise Http404
        form.fields['assembly_status'].queryset = self._get_queryset_for_assembly_status_field()
        return form

    def _get_queryset_for_assembly_status_field(self):
        if self.request.user.has_perm('webapp.change_all_info_about_hazard'):
            queryset = models.AssemblyStatus.objects.all()
        else:
            queryset = models.AssemblyStatus.objects.filter(assembly_status__in=TESTER_ASSEMBLY_STATUSES)
        return queryset


class TestBaseFormView(BaseFormView):
    template_name = 'test/test_form.html'
    form_class = forms.TestForm
    model = models.Test

    def get_success_url(self):
        return reverse('webapp:test_detail', args=(self.object.pk,))

    def get_form(self, form_class):
        form = super(TestBaseFormView, self).get_form(form_class)
        form.fields['tester'].queryset = self._get_queryset_for_tester_field()
        return form

    def _get_queryset_for_tester_field(self):
        queryset = []
        user = self.request.user
        if self.request.user.has_perm('webapp.access_to_own_tests'):
            queryset = models.User.objects.filter(pk=user.pk)
        if self.request.user.has_perm('webapp.access_to_pws_tests'):
            queryset = models.User.objects.filter(groups__name__in=[Groups.tester, Groups.admin],
                                                  employee__pws=user.employee.pws)
        if self.request.user.has_perm('webapp.access_to_all_tests'):
            queryset = models.User.objects.filter(groups__name__in=[Groups.tester, Groups.admin])
        return queryset


class TestAddView(TestBaseFormView, CreateView):
    permission = 'webapp.add_test'
    success_message = Messages.Test.adding_success
    error_message = Messages.Test.adding_error

    def get_context_data(self, **kwargs):
        context = super(TestAddView, self).get_context_data(**kwargs)
        context['hazard'] = models.Hazard.objects.get(pk=self.kwargs['pk'])
        return context

    def get_form(self, form_class):
        if not perm_checkers.HazardPermChecker.has_perm(self.request, models.Hazard.objects.get(pk=self.kwargs['pk'])):
            raise Http404
        return super(TestAddView, self).get_form(form_class)

    def get_success_url(self):
        return reverse('webapp:test_edit', args=(self.object.pk,))

    def form_valid(self, form):
        form.instance.bp_device = models.Hazard.objects.get(pk=self.kwargs['pk'])
        response = super(TestAddView, self).form_valid(form)
        self.request.session['test_for_payment_pk'] = self.object.pk
        return response


class TestEditView(TestBaseFormView, UpdateView):
    permission = 'webapp.change_test'
    success_message = Messages.Test.editing_success
    error_message = Messages.Test.editing_error

    def get_context_data(self, **kwargs):
        context = super(TestEditView, self).get_context_data(**kwargs)
        context['hazard'] = models.Test.objects.get(pk=self.kwargs['pk']).bp_device
        context['test_for_payment_pk'] = self.request.session.get('test_for_payment_pk', None)
        return context

    def get_form(self, form_class):
        form = super(TestEditView, self).get_form(form_class)
        if not perm_checkers.TestPermChecker.has_perm(self.request, form.instance):
            raise Http404
        return form

    def get_initial(self):
        initial = {}
        if not self.object.air_inlet_opened:
            initial['air_inlet_did_not_open'] = True
        if not self.object.rv_opened:
            initial['rv_did_not_open'] = True
        return initial


class UserListView(BaseTemplateView):
    permission = 'webapp.browse_user'
    template_name = 'user/user_list.html'

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['user_list'] = self._get_users()
        return context

    def _get_users(self):
        user_list = OrderedDict()
        if self.request.user.has_perm('webapp.access_to_all_users'):
            user_list['SuperAdministrators'] = models.User.objects.filter(groups__name=Groups.superadmin)
            user_list['Administrators'] = models.User.objects.filter(groups__name=Groups.admin)
            user_list['Surveyors'] = models.User.objects.filter(groups__name=Groups.surveyor)
            user_list['Testers'] = models.User.objects.filter(groups__name=Groups.tester)
            user_list['WithoutGroup'] = models.User.objects.filter(groups__name='')
        elif self.request.user.has_perm('webapp.access_to_pws_users'):
            user_list['Administrators'] = models.User.objects.filter(groups__name=Groups.admin,
                                                                     employee__pws=self.request.user.employee.pws)
            user_list['Surveyors'] = models.User.objects.filter(groups__name=Groups.surveyor,
                                                                employee__pws=self.request.user.employee.pws)
            user_list['Testers'] = models.User.objects.filter(groups__name=Groups.tester,
                                                              employee__pws=self.request.user.employee.pws)
            user_list['WithoutGroup'] = models.User.objects.filter(groups__name='',
                                                                   employee__pws=self.request.user.employee.pws)
        return user_list


class UserBaseFormView(BaseFormView):
    user_model = models.User
    user_object = None
    employee_model = models.Employee
    employee_form_class = forms.EmployeeForm
    employee_object = None
    template_name = 'user/user_form.html'

    def get(self, request, *args, **kwargs):
        user_form = self.get_user_form()
        employee_form = self.get_employee_form()
        user_form.fields['groups'].queryset = self._get_queryset_for_group_field()
        employee_form.fields['pws'].queryset = self._get_queryset_for_pws_field()
        return render(self.request, self.template_name, {'user_form': user_form, 'employee_form': employee_form})

    def _get_queryset_for_group_field(self):
        queryset = []
        if self.request.user.has_perm('webapp.access_to_pws_users'):
            queryset = Group.objects.filter(name__in=ADMIN_GROUPS)
        if self.request.user.has_perm('webapp.access_to_all_users'):
            queryset = Group.objects.all()
        return queryset

    def _get_queryset_for_pws_field(self):
        queryset = []
        if self.request.user.has_perm('webapp.access_to_pws_users'):
            if self.request.user.employee.pws:
                queryset = models.PWS.objects.filter(pk=self.request.user.employee.pws.pk)
        if self.request.user.has_perm('webapp.access_to_all_users'):
            queryset = models.PWS.objects.all()
        return queryset

    def post(self, request, *args, **kwargs):
        user_form = self.get_user_form()
        employee_form = self.get_employee_form()
        if user_form.is_valid() and employee_form.is_valid():
            self.user_object = user_form.save()
            employee_form.instance.user = self.user_object
            if not self.request.user.has_perm('webapp.access_to_all_users'):
                employee_form.instance.pws = self.request.user.pws
            self.employee_object = employee_form.save()
            messages.success(self.request, self.success_message)
            return redirect(self.get_success_url())
        else:
            messages.error(self.request, self.error_message)
            return render(self.request, self.template_name, {'user_form': user_form, 'employee_form': employee_form})

    def get_success_url(self):
        return reverse('webapp:user_list')


class UserAddView(UserBaseFormView):
    permission = 'auth.add_user'
    user_form_class = forms.UserAddForm
    success_message = Messages.User.adding_success
    error_message = Messages.User.adding_error

    def get_user_form(self):
        return self.user_form_class(**self.get_form_kwargs())

    def get_employee_form(self):
        return self.employee_form_class(**self.get_form_kwargs())


class UserEditView(UserBaseFormView):
    permission = 'auth.change_user'
    user_form_class = forms.UserEditForm
    success_message = Messages.User.editing_success
    error_message = Messages.User.editing_error

    def get(self, request, *args, **kwargs):
        response = super(UserEditView, self).get(request, *args, **kwargs)
        if not perm_checkers.UserPermChecker.has_perm(self.request, self.user_object):
            raise Http404
        return response

    def post(self, request, *args, **kwargs):
        user = self.user_model.objects.get(pk=self.kwargs['pk'])
        if not perm_checkers.UserPermChecker.has_perm(self.request, user):
            raise Http404
        return super(UserEditView, self).post(request, *args, **kwargs)

    def get_user_form(self):
        self.user_object = self.user_model.objects.get(pk=self.kwargs['pk'])
        if not perm_checkers.UserPermChecker.has_perm(self.request, self.user_object):
            raise Http404
        return self.user_form_class(instance=self.user_object, **self.get_form_kwargs())

    def get_employee_form(self):
        self.employee_object = self.employee_model.objects.get(user=self.user_object)
        return self.employee_form_class(instance=self.employee_object, **self.get_form_kwargs())


class LetterTypeListView(BaseTemplateView):
    template_name = "letter_type/letter_type_list.html"
    permission = 'webapp.browse_lettertype'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(LetterTypeListView, self).get_context_data(**kwargs)
        lettertypes = self._get_lettertypes(user)
        context['letter_type_list'] = lettertypes
        return context

    def _get_lettertypes(self, user):
        if user.has_perm('webapp.access_to_all_lettertypes'):
            return models.LetterType.objects.all()
        if user.has_perm('webapp.access_to_pws_lettertypes'):
            return models.LetterType.objects.filter(pws=user.employee.pws)
        return []


class LetterTypeBaseFormView(BaseFormView):
    template_name = "letter_type/letter_type_form.html"
    form_class = forms.LetterTypeForm
    model = models.LetterType

    def get_success_url(self):
        return reverse('webapp:letter_type_list')


class LetterTypeEditView(LetterTypeBaseFormView, UpdateView):
    permission = "webapp.access_to_pws_lettertypes"
    success_message = Messages.LetterType.editing_success
    error_message = Messages.LetterType.editing_error

    def get_form(self, form_class):
        form = super(LetterTypeBaseFormView, self).get_form(form_class)
        if perm_checkers.LetterTypePermChecker.has_perm(self.request, form.instance):
            return form
        raise Http404

    def get_context_data(self, **kwargs):
        context = super(LetterTypeEditView, self).get_context_data(**kwargs)
        return context


class LetterListView(BaseTemplateView):
    template_name = "letter/letter_list.html"
    permission = 'webapp.browse_letter'

    def get_context_data(self, **kwargs):
        context = super(LetterListView, self).get_context_data(**kwargs)
        letter_filter = filters.LetterFilter(self.request.GET, queryset=self._get_letter_list())
        context['letter_filter'] = letter_filter
        return context

    def _get_letter_list(self):
        if self.request.user.has_perm('webapp.full_letter_access'):
            return models.Letter.objects.all()
        elif self.request.user.has_perm('webapp.pws_letter_access'):
            return models.Letter.objects.filter(site__pws=self.request.user.employee.pws)
        else:
            raise Http404


class LetterBaseFormView(BaseFormView):
    template_name = "letter/letter_form.html"
    form_class = forms.LetterForm
    model = models.Letter

    def get_success_url(self):
        return reverse("webapp:letter_detail", args=(self.object.pk,))

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super(LetterBaseFormView, self).form_valid(form)
        warnings = LetterRenderer.render(self.object)
        if warnings:
            for warning in warnings:
                messages.warning(self.request, warning)
        else:
            messages.success(self.request, _("All required data is present!"))
        return response


class LetterAddView(LetterBaseFormView, CreateView):
    permission = "webapp.send_letter"
    success_message = Messages.Letter.adding_success
    error_message = Messages.Letter.adding_error

    def get_form(self, form_class):
        site = models.Site.objects.get(pk=self.kwargs['pk'])
        if perm_checkers.SitePermChecker.has_perm(self.request, site):
            form = super(LetterAddView, self).get_form(form_class)
            form.fields['hazard'].queryset = site.hazards.filter(is_present=True)
            form.fields['letter_type'].queryset = site.pws.letter_types
            return form
        raise Http404

    def get_context_data(self, **kwargs):
        context = super(LetterAddView, self).get_context_data(**kwargs)
        context['site'] = models.Site.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.site = models.Site.objects.get(pk=self.kwargs['pk'])
        return super(LetterAddView, self).form_valid(form)


class LetterEditView(LetterBaseFormView, UpdateView):
    permission = "webapp.send_letter"
    success_message = Messages.Letter.editing_success
    error_message = Messages.Letter.editing_error

    def get_form(self, form_class):
        form = super(LetterBaseFormView, self).get_form(form_class)
        if perm_checkers.LetterPermChecker.has_perm(self.request, form.instance):
            site = form.instance.site
            form.fields['hazard'].queryset = site.hazards.filter(is_present=True)
            form.fields['letter_type'].queryset = site.pws.letter_types
            return form
        raise Http404

    def get_context_data(self, **kwargs):
        context = super(LetterEditView, self).get_context_data(**kwargs)
        context['site'] = context['form'].instance.site
        return context


class LetterMixin(object):
    def get_email_body(self, letter, form):
        html = letter.rendered_body

        if form.cleaned_data.get('attach_testers', False):
            testers = models.User.objects.filter(groups__name=Groups.tester, employee__pws=letter.site.pws)
            html += render_to_string('email_templates/html/testers_list.html', {'testers': testers})

        if form.cleaned_data.get('attach_consultant_info', False):
            html += render_to_string('email_templates/html/consultant_info.html', {'pws': letter.site.pws})

        return html


class LetterDetailView(BaseTemplateView, FormView, LetterMixin):
    template_name = "letter/letter_detail.html"
    permission = 'webapp.browse_letter'
    form_class = forms.LetterSendForm
    success_url = 'webapp:letter_list'
    success_message = Messages.Letter.send_success
    error_message = Messages.Letter.send_error

    def get_context_data(self, **kwargs):
        letter = models.Letter.objects.get(pk=self.kwargs['pk'])
        if not perm_checkers.LetterPermChecker.has_perm(self.request, letter):
            raise Http404
        self._set_messages(letter)
        context = super(LetterDetailView, self).get_context_data(**kwargs)
        context['letter'] = letter
        context['form'] = self.form_class(initial={'send_to': letter.site.contact_email})
        return context

    def _set_messages(self, letter):
        if not letter.already_sent:
            warnings = LetterRenderer.render(letter)
            if warnings:
                for warning in warnings:
                    messages.warning(self.request, warning)
            else:
                messages.success(self.request, _("All required data is present!"))
        else:
            messages.info(
                self.request,
                _("This letter has been sent already. \
                If you have changed site or hazard data from this letter and want to send it again, please, \
                open the letter in edit mode and submit the form to regenerate letter content.")
            )

    def form_valid(self, form):
        letter = models.Letter.objects.get(pk=self.kwargs['pk'])
        self._send_email(letter, form)
        return HttpResponseRedirect(reverse(self.success_url))

    def _send_email(self, letter, form):
        body = self.get_email_body(letter, form)

        msg = EmailMessage(
            letter.letter_type.header,
            body,
            to=map(lambda email: email.strip(), form.cleaned_data['send_to'].strip(', ').split(',')),
            headers={'From': settings.DEFAULT_FROM_EMAIL, 'Reply-To': settings.REPLY_TO_EMAIL, 'Return-Path': settings.RETURN_PATH_EMAIL}
        )
        msg.content_subtype = 'html'
        try:
            msg.send()
            messages.success(self.request, self.success_message)
            letter.already_sent = True
            letter.save()
        except SMTPException:
            messages.error(self.request, self.error_message)

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super(LetterDetailView, self).form_invalid(form)


class LetterPDFView(BaseView, FormView, LetterMixin):
    template_name = "letter/letter_pdf_options_modal.html"
    permission = 'webapp.send_letter'
    form_class = forms.LetterOptionsForm

    def get_context_data(self, **kwargs):
        context = super(LetterPDFView, self).get_context_data(**kwargs)
        context['letter'] = models.Letter.objects.get(pk=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            letter = models.Letter.objects.get(pk=self.kwargs['pk'])

            body = self.get_email_body(letter, form)

            pdf_content = PDFGenerator.generate_from_html(body)
            filename = u"%s_%s_%s.pdf" % (letter.date, letter.letter_type.letter_type, letter.site.cust_number)
            return PDFResponse(filename=filename, content=pdf_content)


class HelpView(BaseTemplateView):
    template_name = 'help.html'

    def get_context_data(self, **kwargs):
        context = super(HelpView, self).get_context_data(**kwargs)
        context['user_help'] = models.StaticText.objects.filter(group__in=self.request.user.groups.all())
        context['for_all_help'] = models.StaticText.objects.filter(group=None)
        return context


class SurveyListView(BaseTemplateView):
    template_name = 'survey/survey_list.html'
    permission = "webapp.browse_survey"

    def get_context_data(self, **kwargs):
        context = super(SurveyListView, self).get_context_data(**kwargs)
        surveys = self._get_survey_list()
        context['survey_filter'] = filters.SurveyFilter(self.request.GET, queryset=surveys)
        return context

    def _get_survey_list(self):
        user = self.request.user
        if user.has_perm("webapp.access_to_all_surveys"):
            return models.Survey.objects.all()
        if user.has_perm("webapp.access_to_pws_surveys"):
            return models.Survey.objects.filter(site__pws=user.employee.pws)
        if user.has_perm("webapp.access_to_own_surveys"):
            return models.Survey.objects.filter(surveyor=user, site__pws=user.employee.pws)


class HazardListView(BaseTemplateView):
    template_name = 'hazard/hazard_list.html'
    permission = "webapp.browse_hazard"

    def get_context_data(self, **kwargs):
        context = super(HazardListView, self).get_context_data(**kwargs)
        hazards = self._get_hazard_list()
        context['hazard_filter'] = filters.HazardFilter(self.request.GET, queryset=hazards)
        return context

    def _get_hazard_list(self):
        user = self.request.user
        queryset = models.Hazard.objects.none()
        if user.has_perm('webapp.access_to_all_hazards'):
            queryset = models.Hazard.objects.all()
        elif user.has_perm('webapp.access_to_pws_hazards'):
            queryset = (models.Hazard.objects.filter(site__pws=user.employee.pws, is_present=True) |
                        models.Hazard.objects.filter(tests__tester=user)).distinct()
        sql_query_for_priority = HazardPriorityQuery.get_query(connection.vendor)
        return queryset.extra(select={'priority': sql_query_for_priority}, order_by=('priority',))


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
            return paid_tests.filter(bp_device__site__pws=user.employee.pws)
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
        context['test'] = test
        context['hazard'] = test.bp_device
        return context


class UnpaidTestMixin(object):
    def get_unpaid_tests(self):
        user = self.request.user
        paid_tests = models.Test.objects.filter(paid=False)
        if user.has_perm('webapp.access_to_all_tests'):
            return paid_tests
        if user.has_perm("webapp.access_to_pws_tests"):
            return paid_tests.filter(bp_device__site__pws=user.employee.pws)
        if user.has_perm('webapp.access_to_own_tests'):
            return paid_tests.filter(tester=user)


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
                models.Test.objects.filter(pk__in=test_pks).update(paid=True)
                messages.success(self.request, __(Messages.Test.payment_successful_singular, Messages.Test.payment_successful_plural, len(test_pks)))
            else:
                messages.error(self.request, Messages.Test.payment_failed)
        else:
            messages.error(self.request, Messages.Test.payment_cancelled)
        return redirect(reverse('webapp:unpaid_test_list'))

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


class TesterListView(BaseTemplateView):
    template_name = 'user/tester_list.html'
    permission = 'webapp.browse_user'

    def get_context_data(self, **kwargs):
        context = super(TesterListView, self).get_context_data(**kwargs)
        testers = self._get_testers()
        context['tester_filter'] = filters.TesterFilter(self.request.GET, queryset=testers)
        return context

    def _get_testers(self):
        user = self.request.user
        if user.has_perm('webapp.access_to_all_users'):
            return models.User.objects.filter(groups__name=Groups.tester)
        if user.has_perm('webapp.access_to_pws_users'):
            return models.User.objects.filter(groups__name=Groups.tester, employee__pws=user.employee.pws)


class UserDetailView(BaseTemplateView):
    template_name = "user/user_detail.html"
    permission = "webapp.browse_user"

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        selected_user = User.objects.get(pk=kwargs['pk'])
        if perm_checkers.UserPermChecker.has_perm(self.request, selected_user):
            context['selected_user'] = selected_user
            if Group.objects.get(name=Groups.tester) in selected_user.groups.all():
                context['is_tester'] = True
            return context
        raise Http404


class ImportView(BaseFormView):
    permission = 'webapp.access_to_import'
    template_name = 'import/import.html'
    form_class = ImportForm

    def get_form(self, form_class):
        form = super(ImportView, self).get_form(form_class)
        if self.request.user.has_perm('webapp.access_to_all_sites'):
            form.fields['pws'] = ModelChoiceField(queryset=models.PWS.objects.all())
        return form

    def get_context_data(self, **kwargs):
        context = super(ImportView, self).get_context_data(**kwargs)
        context['dateformat_help'] = DATEFORMAT_HELP
        return context

    def form_valid(self, form):
        self._delete_previous_tmp_files()
        filename = self._save_tmp_file(form.cleaned_data.get('file'))
        self.request.session['import_filename'] = filename
        if form.cleaned_data.get('date_format') == OTHER:
            self.request.session['import_date_format'] = form.cleaned_data.get('date_format_other')
        else:
            self.request.session['import_date_format'] = form.cleaned_data.get('date_format')
        try:
            self.request.session['import_pws_pk'] = form.cleaned_data['pws'].pk
        except KeyError:
            self.request.session['import_pws_pk'] = self.request.user.employee.pws.pk
        self._delete_cached_data()
        return super(ImportView, self).form_valid(form)

    def _delete_previous_tmp_files(self):
        prefix = '%s-' % self.request.user.pk
        files = os.listdir(settings.EXCEL_FILES_DIR)
        for file in files:
            if file.startswith(prefix):
                os.unlink(os.path.join(settings.EXCEL_FILES_DIR, file))

    def _save_tmp_file(self, file):
        name, ext = os.path.splitext(file.name)
        new_filename = '%s-%s%s' % (self.request.user.pk, int(time.time()), ext)
        default_storage.save(os.path.join(settings.EXCEL_FILES_DIR, new_filename), file)
        return new_filename

    def _delete_cached_data(self):
        self.request.session.pop('cached_excel_headers', None)
        self.request.session.pop('cached_excel_example_rows', None)

    def get_success_url(self):
        return reverse('webapp:import-mappings')


class ImportMappingsFormsetMixin(BaseTemplateView):
    permission = 'webapp.access_to_import'
    template_name = 'import/import_mappings.html'
    form_class = ImportMappingsForm
    base_formset_class = BaseImportMappingsFormSet

    EXAMPLE_ROWS_COUNT = 3

    exclude_site_model_fields = ['id', 'pws']
    formset = None
    excel_parser = None

    def get_site_model_fields_list(self):
        field_names = []
        for field in models.Site._meta.fields:
            if field.name not in self.exclude_site_model_fields:
                field_names.append(field.name)
        return field_names

    def get_site_model_fields_labels(self, fields_list):
        field_labels = []
        for field in models.Site._meta.fields:
            if field.name in fields_list:
                field_labels.append(field.verbose_name)
        return field_labels

    def get_site_model_fields_help_texts(self, fields_list):
        field_help_texts = []
        for field in models.Site._meta.fields:
            if field.name in fields_list:
                field_help_texts.append(field.help_text)
        return field_help_texts

    def get_site_model_required_fields(self, fields_list):
        required_fields = []
        for field in models.Site._meta.fields:
            if field.name in fields_list and (not field.null and field.default == NOT_PROVIDED):
                required_fields.append(field.name)
        return required_fields

    def get_excel_field_headers_as_choices(self):
        if 'cached_excel_headers' in self.request.session:
            return self.request.session['cached_excel_headers']
        headers = self.excel_parser.get_headers_as_choices()
        self.request.session['cached_excel_headers'] = headers
        return headers

    def get_excel_example_rows(self, rows_count=EXAMPLE_ROWS_COUNT):
        if 'cached_excel_example_rows' in self.request.session:
            return self.request.session['cached_excel_example_rows']
        example_rows = self.excel_parser.get_example_rows(rows_count)
        self.request.session['cached_excel_example_rows'] = example_rows
        return example_rows

    def get_formset(self):
        self.excel_parser = ExcelParser(os.path.join(settings.EXCEL_FILES_DIR, self.request.session['import_filename']))

        formset_class = formset_factory(form=self.form_class, formset=self.base_formset_class, extra=0)

        model_fields_list = self.get_site_model_fields_list()

        model_fields_for_form = [{'model_field': field_name} for field_name in model_fields_list]
        formset = formset_class(initial=model_fields_for_form, data=self.get_formset_data())

        model_fields_labels = self.get_site_model_fields_labels(model_fields_list)
        formset.set_model_fields_labels(model_fields_labels)

        model_fields_help_texts = self.get_site_model_fields_help_texts(model_fields_list)
        formset.set_model_fields_help_texts(model_fields_help_texts)

        model_required_fields = self.get_site_model_required_fields(model_fields_list)
        formset.set_required_model_fields(model_required_fields)

        excel_field_choices = self.get_excel_field_headers_as_choices()
        sorted_excel_field_choices = sorted(excel_field_choices, key=lambda item: item[1])
        formset.set_excel_field_choices(sorted_excel_field_choices)

        return formset

    def get_context_data(self, **kwargs):
        context = super(ImportMappingsFormsetMixin, self).get_context_data(**kwargs)
        context['formset'] = self.formset
        context['rows_count'] = (self.formset.total_form_count() - 1) / 2 + 1
        context['excel_example_rows'] = self.get_excel_example_rows()
        context['excel_field_headers'] = self.get_excel_field_headers_as_choices()
        if 'import_mappings' in self.request.session:
            context['import_mappings'] = json.dumps(self.request.session['import_mappings'])
        return context

    def get_formset_data(self):
        return None


class ImportMappingsRenderView(ImportMappingsFormsetMixin):
    def get(self, request, *args, **kwargs):
        self.formset = self.get_formset()
        return self.render_to_response(self.get_context_data())


class ImportMappingsProcessView(ImportMappingsFormsetMixin):
    def post(self, request, *args, **kwargs):
        self.formset = self.get_formset()
        if self.formset.is_valid():
            return self._import_excel_file()
        else:
            return self.render_to_response(self.get_context_data())

    def _import_excel_file(self):
        mappings = self.formset.get_mappings()
        self.request.session['import_mappings'] = mappings
        try:
            self._try_to_import(mappings)
            return redirect('webapp:import-mappings')
        except (IntegrityError, DateFormatError) as e:
            self.formset.add_error(str(e))
            return self.render_to_response(self.get_context_data())

    def _try_to_import(self, mappings):
        pws = models.PWS.objects.get(pk=self.request.session.pop('import_pws_pk'))
        date_format = self.request.session.pop('import_date_format')
        self.excel_parser.check_constraints(mappings, date_format)
        import_log = models.ImportLog.objects.create(user=self.request.user, pws=pws)
        self.request.session['import_log_pk'] = import_log.pk
        self._run_background_parser(self.request.session['import_filename'], date_format, import_log, mappings)


    def _run_background_parser(self, filename, date_format, import_log, mappings):
        background_runner = BackgroundExcelParserRunner()
        background_runner.filename = filename
        background_runner.mappings = mappings
        background_runner.date_format = date_format
        background_runner.import_log_pk = import_log.pk
        background_runner.execute()

    def get_formset_data(self):
        return self.request.POST


class ImportProgressView(BaseTemplateView):
    permission = 'webapp.access_to_import'

    def get(self, request, *args, **kwargs):
        import_log_pk = self.request.session['import_log_pk']
        import_log = models.ImportLog.objects.get(pk=import_log_pk)
        progress = import_log.progress
        if import_log.progress == FINISHED:
            del self.request.session['import_log_pk']
        return JsonResponse({'progress': progress})


class ImportLogListView(BaseTemplateView):
    permission = 'webapp.browse_import_log'
    template_name = 'import/import_log_list.html'

    def get_context_data(self, **kwargs):
        context = super(ImportLogListView, self).get_context_data(**kwargs)
        context['import_logs'] = self._get_import_logs()
        return context

    def _get_import_logs(self):
        queryset = models.ImportLog.objects.none()
        if self.request.user.has_perm('webapp.access_to_all_import_logs'):
            queryset = models.ImportLog.objects.all()
        elif self.request.user.has_perm('webapp.access_to_pws_import_logs'):
            queryset = models.ImportLog.objects.filter(pws=self.request.user.employee.pws)
        return queryset.order_by('-datetime')


class ImportLogSitesMixin(BaseTemplateView):
    permission = 'webapp.browse_import_log'
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(ImportLogSitesMixin, self).get_context_data(**kwargs)
        import_log = models.ImportLog.objects.get(pk=self.kwargs['pk'])
        if not perm_checkers.ImportLogPermChecker.has_perm(self.request, import_log):
            raise Http404
        context['import_log'] = import_log
        sites = self.get_sites(import_log)
        context['site_filter'] = filters.SiteFilter(self.request.GET, queryset=sites)
        return context


class ImportLogAddedSitesView(ImportLogSitesMixin):
    def get_sites(self, import_log):
        return import_log.added_sites


class ImportLogUpdatedSitesView(ImportLogSitesMixin):
    def get_sites(self, import_log):
        return import_log.updated_sites


class ImportLogDeactivatedSitesView(ImportLogSitesMixin):
    def get_sites(self, import_log):
        return import_log.deactivated_sites