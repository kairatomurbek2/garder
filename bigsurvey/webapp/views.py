from collections import OrderedDict
from django.views.generic import TemplateView, CreateView, UpdateView
from django.views.generic.edit import ModelFormMixin, ProcessFormView
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from webapp import mixins, models, forms, filters
from main.parameters import Messages, Groups, TESTER_ASSEMBLY_STATUSES, ADMIN_GROUPS, ServiceTypes
from django.views.decorators.csrf import csrf_exempt


class BaseView(mixins.PermissionRequiredMixin):
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
        if user.has_perm('webapp.access_to_survey_sites'):
            inspections = models.Inspection.objects.filter(assigned_to=user, is_active=True)
            return self._filter_sites_by_related(inspections)
        return []

    @staticmethod
    def _filter_sites_by_related(related):
        site_pks = [obj.site.pk for obj in related]
        return models.Site.objects.filter(pk__in=site_pks)


class SiteDetailView(BaseTemplateView):
    template_name = 'site/site.html'
    permission = 'webapp.browse_site'

    def get_context_data(self, **kwargs):
        site = models.Site.objects.get(pk=self.kwargs['pk'])
        if not mixins.SiteObjectMixin.has_perm(self.request, site):
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

    def post(self, request, *args, **kwargs):
        user = self.request.user
        site = models.Site.objects.get(pk=kwargs['pk'])
        if user.has_perm('webapp.access_to_survey_sites'):
            models.Inspection.objects.filter(site=site, assigned_to=user, is_active=True).update(is_active=False)
        return redirect(reverse("webapp:home"))

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(SiteDetailView, self).dispatch(*args, **kwargs)


class SiteBaseFormView(BaseFormView):
    template_name = 'site/site_form.html'
    form_class = forms.SiteForm
    model = models.Site
    filter_class = filters.CustomerFilter

    def get_context_data(self, **kwargs):
        context = super(SiteBaseFormView, self).get_context_data(**kwargs)
        customers = self._get_customers()
        context['customer_filter'] = self._get_customer_filter(queryset=customers)
        return context

    @staticmethod
    def _get_customers():
        return models.Customer.objects.all()

    def _get_customer_filter(self, queryset):
        return self.filter_class(self.request.GET, queryset=queryset)

    def get_form(self, form_class):
        form = super(SiteBaseFormView, self).get_form(form_class)
        if not self.request.user.has_perm('webapp.access_to_all_sites'):
            form.fields['pws'].queryset = models.PWS.objects.filter(pk=self.request.user.employee.pws.pk)
        return form

    def get_success_url(self):
        return reverse('webapp:home')


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
        if not mixins.SiteObjectMixin.has_perm(self.request, form.instance):
            raise Http404
        form.initial['customer'] = form.instance.customer.pk
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
            self._batch_update_hazards_for_site(date, site_pk)

    def _batch_update_hazards_for_site(self, date, site_pk):
        for service_type in models.ServiceType.objects.all():
            try:
                survey = models.Survey.objects.filter(site__pk=site_pk, service_type=service_type).latest('survey_date')
                survey.hazards.update(due_install_test_date=date)
            except models.Survey.DoesNotExist:
                pass

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


class CustomerListView(BaseTemplateView):
    template_name = 'customer/customer_list.html'
    permission = 'webapp.browse_customer'

    def get_context_data(self, **kwargs):
        context = super(CustomerListView, self).get_context_data(**kwargs)
        customers = self._get_customers()
        context['customer_filter'] = self._get_customer_filter(queryset=customers)
        return context

    @staticmethod
    def _get_customers():
        return models.Customer.objects.all()

    def _get_customer_filter(self, queryset):
        return filters.CustomerFilter(self.request.GET, queryset=queryset)


class CustomerDetailView(BaseTemplateView):
    template_name = 'customer/customer.html'
    permission = 'webapp.browse_customer'

    def get_context_data(self, **kwargs):
        context = super(CustomerDetailView, self).get_context_data(**kwargs)
        context['customer'] = self._get_customer()
        return context

    def _get_customer(self):
        return models.Customer.objects.get(pk=self.kwargs['pk'])


class CustomerBaseFormView(BaseFormView):
    template_name = 'customer/customer_form.html'
    form_class = forms.CustomerForm
    model = models.Customer

    def get_success_url(self):
        return reverse('webapp:customer_list')


class CustomerAddView(CustomerBaseFormView, CreateView):
    permission = 'webapp.add_customer'
    success_message = Messages.Customer.adding_success
    error_message = Messages.Customer.adding_error


class CustomerEditView(CustomerBaseFormView, UpdateView):
    permission = 'webapp.change_customer'
    success_message = Messages.Customer.editing_success
    error_message = Messages.Customer.editing_error


class SurveyDetailView(BaseTemplateView):
    template_name = 'survey/survey.html'
    permission = 'webapp.browse_survey'

    def get_context_data(self, **kwargs):
        survey = models.Survey.objects.get(pk=self.kwargs['pk'])
        if not mixins.SurveyObjectMixin.has_perm(self.request, survey):
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
            if hazard in form.instance.hazards.all():
                hazard.is_present = True
            else:
                hazard.is_present = False
            hazard.save()
        return HttpResponseRedirect(self.get_success_url())

    def _get_site(self):
        site = models.Site.objects.get(pk=self.kwargs['pk'])
        if not mixins.SiteObjectMixin.has_perm(self.request, site):
            raise Http404
        return site

    def _get_service_type(self):
        return models.ServiceType.objects.filter(service_type__icontains=self.kwargs['service'])[0]

    def get_form(self, form_class):
        if not mixins.SiteObjectMixin.has_perm(self.request, self._get_site()):
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
        if not mixins.SurveyObjectMixin.has_perm(self.request, form.instance):
            raise Http404
        return form

    def form_valid(self, form):
        site = form.instance.site
        super(SurveyEditView, self).form_valid(form)
        survey = site.surveys.latest('survey_date')
        site.last_survey_date = survey.survey_date
        site.save()
        for hazard in site.hazards.all():
            if hazard in form.instance.hazards.all():
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
        if not mixins.HazardObjectMixin.has_perm(self.request, hazard):
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
        if not mixins.SiteObjectMixin.has_perm(self.request, site):
            raise Http404
        return super(HazardAddView, self).get_form(form_class)

    def form_valid(self, form):
        form.instance.site = models.Site.objects.get(pk=self.kwargs['pk'])
        form.instance.service_type = models.ServiceType.objects.get(service_type=self.kwargs['service'])
        return super(HazardAddView, self).form_valid(form)


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
        if not mixins.HazardObjectMixin.has_perm(self.request, form.instance):
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

    def get_context_data(self, **kwargs):
        context = super(TestBaseFormView, self).get_context_data(**kwargs)
        context['hazard'] = models.Hazard.objects.get(pk=self.kwargs['pk'])
        return context

    def get_form(self, form_class):
        form = super(TestBaseFormView, self).get_form(form_class)
        form.fields['tester'].queryset = self._get_queryset_for_tester_field()
        return form

    def _get_queryset_for_tester_field(self):
        queryset = []
        if self.request.user.has_perm('webapp.access_to_own_tests'):
            queryset = models.User.objects.filter(pk=self.request.user.pk)
        if self.request.user.has_perm('webapp.access_to_pws_tests'):
            queryset = models.User.objects.filter(groups__name=Groups.tester, employee__pws=self.request.user.employee.pws)
        if self.request.user.has_perm('webapp.access_to_all_tests'):
            queryset = models.User.objects.filter(groups__name=Groups.tester)
        return queryset


class TestAddView(TestBaseFormView, CreateView):
    permission = 'webapp.add_test'
    success_message = Messages.Test.adding_success
    error_message = Messages.Test.adding_error

    def get_form(self, form_class):
        if not mixins.HazardObjectMixin.has_perm(self.request, models.Hazard.objects.get(pk=self.kwargs['pk'])):
            raise Http404
        return super(TestAddView, self).get_form(form_class)

    def form_valid(self, form):
        form.instance.bp_device = models.Hazard.objects.get(pk=self.kwargs['pk'])
        return super(TestAddView, self).form_valid(form)


class TestEditView(TestBaseFormView, UpdateView):
    permission = 'webapp.change_test'
    success_message = Messages.Test.editing_success
    error_message = Messages.Test.editing_error

    def get_form(self, form_class):
        form = super(TestEditView, self).get_form(form_class)
        if not mixins.TestObjectMixin.has_perm(self.request, form.instance):
            raise Http404
        return form


class InspectionListView(BaseTemplateView):
    permission = 'webapp.browse_inspection'
    template_name = 'inspection/inspection_list.html'

    def get_context_data(self, **kwargs):
        context = super(InspectionListView, self).get_context_data(**kwargs)
        context['inspection_list'] = self._get_inspections()
        return context

    def _get_inspections(self):
        inspections = []
        if self.request.user.has_perm('webapp.access_to_pws_inspections'):
            inspections = models.Inspection.objects.filter(site__pws=self.request.user.employee.pws)
        if self.request.user.has_perm('webapp.access_to_all_inspections'):
            inspections = models.Inspection.objects.all()
        return inspections


class InspectionBaseFormView(BaseFormView):
    model = models.Inspection
    form_class = forms.InspectionForm
    template_name = 'inspection/inspection_form.html'

    def get_success_url(self):
        return reverse('webapp:home')

    def get_form(self, form_class):
        form = super(InspectionBaseFormView, self).get_form(form_class)
        form.fields['assigned_to'].queryset = self._get_queryset_for_assigned_to_field()
        return form

    def _get_queryset_for_assigned_to_field(self):
        queryset = []
        if self.request.user.has_perm('webapp.access_to_pws_inspections'):
            queryset = models.User.objects.filter(groups__name=Groups.surveyor, employee__pws=self.request.user.employee.pws)
        if self.request.user.has_perm('webapp.access_to_all_inspections'):
            queryset = models.User.objects.filter(groups__name=Groups.surveyor)
        return queryset


class InspectionAddView(InspectionBaseFormView, CreateView):
    permission = 'webapp.add_inspection'
    success_message = Messages.Inspection.adding_success
    error_message = Messages.Inspection.adding_error

    def get_form(self, form_class):
        site = models.Site.objects.get(pk=self.kwargs['pk'])
        if not mixins.SiteObjectMixin.has_perm(self.request, site):
            raise Http404
        return super(InspectionAddView, self).get_form(form_class)

    def form_valid(self, form):
        form.instance.assigned_by = self.request.user
        form.instance.site = self._get_site()
        form.instance.is_active = True
        return super(InspectionAddView, self).form_valid(form)

    def _get_site(self):
        site = models.Site.objects.get(pk=self.kwargs['pk'])
        if not mixins.SiteObjectMixin.has_perm(self.request, site):
            raise Http404
        return site


class InspectionEditView(InspectionBaseFormView, UpdateView):
    permission = 'webapp.change_inspection'
    success_message = Messages.Inspection.editing_success
    error_message = Messages.Inspection.editing_error

    def get_form(self, form_class):
        form = super(InspectionEditView, self).get_form(form_class)
        if not mixins.InspectionObjectMixin.has_perm(self.request, form.instance):
            raise Http404
        return form


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
        if not mixins.UserObjectMixin.has_perm(self.request, self.user_object):
            raise Http404
        return response

    def post(self, request, *args, **kwargs):
        user = self.user_model.objects.get(pk=self.kwargs['pk'])
        if not mixins.UserObjectMixin.has_perm(self.request, user):
            raise Http404
        return super(UserEditView, self).post(request, *args, **kwargs)

    def get_user_form(self):
        self.user_object = self.user_model.objects.get(pk=self.kwargs['pk'])
        if not mixins.UserObjectMixin.has_perm(self.request, self.user_object):
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
        context['letters'] = models.Letter.objects.all()
        return context


class LetterSendView(BaseFormView):
    template_name = "letter_send.html"
    form_class = forms.LetterSendForm
    permission = 'webapp.send_letter'


class LetterDetailView(BaseTemplateView):
    template_name = "letter/letter_detail.html"

    def get_context_data(self, **kwargs):
        context = super(LetterDetailView, self).get_context_data(**kwargs)
        context['letter'] = models.Letter.objects.get(pk=kwargs['pk'])
        return context


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
            return models.Survey.objects.filter(surveyor=user)


class HazardListView(BaseTemplateView):
    pass


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
            return models.Test.objects.filter(tester=user)


class TestDetailView(BaseTemplateView):
    pass


class UserDetailView(BaseTemplateView):
    pass