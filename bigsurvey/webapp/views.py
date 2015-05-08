from collections import OrderedDict
from django.views.generic import TemplateView, CreateView, UpdateView, FormView, View
from django.views.generic.edit import ModelFormMixin, ProcessFormView
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from webapp import perm_checkers, models, forms, filters
from main.parameters import Messages, Groups, TESTER_ASSEMBLY_STATUSES, ADMIN_GROUPS, ServiceTypes
from django.contrib.auth.models import User
from webapp.utils.letter_renderer import LetterRenderer
from webapp.forms import TesterSiteSearchForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.core.mail import EmailMessage
from webapp.utils.pdf_generator import PDFGenerator


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


class BaseFormView(BaseView, ModelFormMixin, ProcessFormView):
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
        return redirect(reverse('webapp:site_detail', args=(form.site.pk,)))


class SiteDetailView(BaseTemplateView):
    template_name = 'site/site.html'
    permission = 'webapp.browse_site'

    def get_context_data(self, **kwargs):
        site = models.Site.objects.get(pk=self.kwargs['pk'])
        if not perm_checkers.SitePermChecker.has_perm(self.request, site):
            raise Http404
        surveys_potable = site.surveys.filter(service_type__service_type=ServiceTypes.potable)
        surveys_fire = site.surveys.filter(service_type__service_type=ServiceTypes.fire)
        surveys_irrigation = site.surveys.filter(service_type__service_type=ServiceTypes.irrigation)
        hazards_potable = site.hazards.filter(service_type__service_type=ServiceTypes.potable, is_present=True)
        hazards_fire = site.hazards.filter(service_type__service_type=ServiceTypes.fire, is_present=True)
        hazards_irrigation = site.hazards.filter(service_type__service_type=ServiceTypes.irrigation, is_present=True)
        context = super(SiteDetailView, self).get_context_data(**kwargs)
        context['site'] = site
        context['surv_p'] = surveys_potable
        context['surv_f'] = surveys_fire
        context['surv_i'] = surveys_irrigation
        context['haz_p'] = hazards_potable
        context['haz_f'] = hazards_fire
        context['haz_i'] = hazards_irrigation
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

    def get_form(self, form_class):
        form = super(SurveyBaseFormView, self).get_form(form_class)
        form.fields['surveyor'].queryset = self._get_queryset_for_surveyor_field()
        form.fields['hazards'].queryset = self._get_queryset_for_hazards_field(form.instance)
        return form

    def _get_queryset_for_hazards_field(self, survey):
        try:
            site = survey.site
            service_type = survey.service_type
        except:
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
        super(SurveyAddView, self).form_valid(form)
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
        if not self._service_type_on_site_exists():
            raise Http404
        return super(SurveyAddView, self).get_form(form_class)

    def _service_type_on_site_exists(self):
        site = models.Site.objects.get(pk=self.kwargs['pk'])
        service_type = self.kwargs['service']
        if service_type == 'potable' and site.potable_present:
            return True
        if service_type == 'fire' and site.fire_present:
            return True
        if service_type == 'irrigation' and site.irrigation_present:
            return True
        return False


class SurveyEditView(SurveyBaseFormView, UpdateView):
    permission = 'webapp.add_survey'
    success_message = Messages.Survey.editing_success
    error_message = Messages.Survey.editing_error

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
        tests_count = models.Test.objects.filter(bp_device=hazard, tester=self.request.user).count()
        return tests_count <= 0


class HazardBaseFormView(BaseFormView):
    template_name = 'hazard/hazard_form.html'
    form_class = forms.HazardForm
    form_class_for_tester = forms.HazardFormForTester
    model = models.Hazard

    def get_success_url(self):
        return reverse('webapp:hazard_detail', args=(self.object.pk,))


class HazardAddView(HazardBaseFormView, CreateView):
    permission = 'webapp.add_hazard'
    success_message = Messages.Hazard.adding_success
    error_message = Messages.Hazard.adding_error

    def get_context_data(self, **kwargs):
        context = super(HazardAddView, self).get_context_data(**kwargs)
        context['site_pk'] = self.kwargs['pk']
        return context

    def get_form(self, form_class):
        site = models.Site.objects.get(pk=self.kwargs['pk'])
        if not perm_checkers.SitePermChecker.has_perm(self.request, site):
            raise Http404
        if not self._service_type_on_site_exists():
            raise Http404
        return super(HazardAddView, self).get_form(form_class)

    def form_valid(self, form):
        form.instance.site = models.Site.objects.get(pk=self.kwargs['pk'])
        form.instance.service_type = models.ServiceType.objects.get(service_type=self.kwargs['service'])
        return super(HazardAddView, self).form_valid(form)

    def _service_type_on_site_exists(self):
        site = models.Site.objects.get(pk=self.kwargs['pk'])
        service_type = self.kwargs['service']
        if service_type == 'potable' and site.potable_present:
            return True
        if service_type == 'fire' and site.fire_present:
            return True
        if service_type == 'irrigation' and site.irrigation_present:
            return True
        return False


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
        return reverse('webapp:hazard_detail', args=(self.kwargs['pk'],))

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

    def form_valid(self, form):
        form.instance.bp_device = models.Hazard.objects.get(pk=self.kwargs['pk'])
        return super(TestAddView, self).form_valid(form)


class TestEditView(TestBaseFormView, UpdateView):
    permission = 'webapp.change_test'
    success_message = Messages.Test.editing_success
    error_message = Messages.Test.editing_error

    def get_context_data(self, **kwargs):
        context = super(TestEditView, self).get_context_data(**kwargs)
        context['hazard'] = models.Test.objects.get(pk=self.kwargs['pk']).bp_device
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
            user_list['Administrators'] = models.User.objects.filter(groups__name=Groups.admin, employee__pws=self.request.user.employee.pws)
            user_list['Surveyors'] = models.User.objects.filter(groups__name=Groups.surveyor, employee__pws=self.request.user.employee.pws)
            user_list['Testers'] = models.User.objects.filter(groups__name=Groups.tester, employee__pws=self.request.user.employee.pws)
            user_list['WithoutGroup'] = models.User.objects.filter(groups__name='', employee__pws=self.request.user.employee.pws)
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
            form = super(LetterBaseFormView, self).get_form(form_class)
            form.fields['hazard'].queryset = site.hazards.filter(is_present=True)
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
            return form
        raise Http404

    def get_context_data(self, **kwargs):
        context = super(LetterEditView, self).get_context_data(**kwargs)
        context['site'] = context['form'].instance.site
        return context


class LetterDetailView(BaseTemplateView, FormView):
    template_name = "letter/letter_detail.html"
    permission = 'webapp.browse_letter'
    form_class = forms.LetterSendForm
    success_url = 'webapp:letter_list'
    success_message = Messages.Letter.send_success
    error_message = Messages.Letter.send_error

    def get_context_data(self, **kwargs):
        letter = models.Letter.objects.get(pk=self.kwargs['pk'])
        if perm_checkers.LetterPermChecker.has_perm(self.request, letter):
            self._set_messages(letter)
            context = super(LetterDetailView, self).get_context_data(**kwargs)
            context['letter'] = letter
            # for some reason (maybe inheritance issue)
            # default get_form method is not called in super's get_context_data
            # so here it's done manually with our own method _get_form
            if not context.get('form'):
                context['form'] = self._get_form(letter)
            return context
        raise Http404

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

    def _get_form(self, letter):
        return self.form_class(initial={
            'send_to': "" or unicode(letter.site.contact_email)
        })

    def form_valid(self, form):
        letter = models.Letter.objects.get(pk=self.kwargs['pk'])
        self._send_email(letter, form)
        return HttpResponseRedirect(reverse(self.success_url))

    def _send_email(self, letter, form):
        msg = EmailMessage(
            letter.letter_type.header,
            letter.rendered_body,
            to=[form.cleaned_data['send_to']]
        )
        msg.content_subtype = 'html'
        try:
            msg.send()
            messages.success(self.request, self.success_message)
            letter.already_sent = True
            letter.save()
        except:
            messages.error(self.request, self.error_message)

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super(LetterDetailView, self).form_invalid(form)


class LetterPDFView(BaseView):
    template_name = "letter/pdf.html"
    permission = 'webapp.send_letter'

    def get(self, request, *args, **kwargs):
        letter = models.Letter.objects.get(pk=kwargs['pk'])
        pdf = PDFGenerator.generate_letter(letter)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = u'attachment; filename="%s_%s_%s.pdf"' % (
            letter.date,
            letter.letter_type.letter_type,
            letter.site.cust_number
        )
        return response


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
        if user.has_perm('webapp.access_to_all_hazards'):
            return models.Hazard.objects.all()
        if user.has_perm('webapp.access_to_pws_hazards'):
            return models.Hazard.objects.filter(site__pws=user.employee.pws, is_present=True)


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
        if user.has_perm('webapp.access_to_all_tests'):
            return models.Test.objects.all()
        if user.has_perm("webapp.access_to_pws_tests"):
            return models.Test.objects.filter(bp_device__site__pws=user.employee.pws)
        if user.has_perm('webapp.access_to_own_tests'):
            return models.Test.objects.filter(tester=user, bp_device__site__pws=user.employee.pws)


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