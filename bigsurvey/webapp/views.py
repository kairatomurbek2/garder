from django.views.generic import TemplateView, View, CreateView, UpdateView
from django.views.generic.edit import ModelFormMixin, ProcessFormView
import models
import forms
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from filters import SiteFilter, CustomerFilter
from django.http import Http404
from django.core.urlresolvers import reverse
from abc import ABCMeta, abstractmethod
from django.contrib import messages
from main.parameters import Messages, Groups, TESTER_ASSEMBLY_STATUSES


class AccessRequiredMixin(View):
    permission = None

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.permission:
            if not self.request.user.has_perm(self.permission):
                raise Http404
        return super(AccessRequiredMixin, self).dispatch(*args, **kwargs)


class BaseView(AccessRequiredMixin):
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


class ObjectPermissionMixin(object):
    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def has_perm(request, obj):
        pass


class SiteObjectPermissionMixin(ObjectPermissionMixin):
    @staticmethod
    def has_perm(request, obj):
        return request.user.has_perm('webapp.access_to_all_sites') or \
               request.user.has_perm('webapp.access_to_pws_sites') and obj.pws == request.user.employee.pws or \
               request.user.has_perm('webapp.access_to_survey_sites') and obj.inspections.filter(
                   assigned_to=request.user) or \
               request.user.has_perm('webapp.access_to_test_sites') and obj.test_perms.filter(given_to=request.user)


class SurveyObjectPermissionMixin(ObjectPermissionMixin):
    @staticmethod
    def has_perm(request, obj):
        return request.user.has_perm('webapp.access_to_all_surveys') or \
               request.user.has_perm('webapp.access_to_pws_surveys') and obj.site.pws == request.user.employee.pws or \
               request.user.has_perm('webapp.access_to_own_surveys') and obj.surveyor == request.user


class HazardObjectPermissionMixin(ObjectPermissionMixin):
    @staticmethod
    def has_perm(request, obj):
        return request.user.has_perm('webapp.access_to_all_hazards') or \
               request.user.has_perm(
                   'webapp.access_to_pws_hazards') and obj.survey.site.pws == request.user.employee.pws or \
               request.user.has_perm('webapp.access_to_own_hazards') and obj.survey.surveyor == request.user or \
               request.user.has_perm('webapp.access_to_site_hazards') and models.TestPermission.objects.filter(
                   site=obj.survey.site, given_to=request.user)


class TestObjectPermissionMixin(ObjectPermissionMixin):
    @staticmethod
    def has_perm(request, obj):
        return request.user.has_perm('webapp.access_to_all_tests') or \
               request.user.has_perm(
                   'webapp.access_to_pws_tests') and obj.bp_service.survey.site.pws == request.user.employee.pws or \
               request.user.has_perm('webapp.access_to_own_tests') and obj.tester == request.user


class InspectionObjectPermissionMixin(ObjectPermissionMixin):
    @staticmethod
    def has_perm(request, obj):
        return request.user.has_perm('webapp.access_to_all_inspections') or \
               request.user.has_perm('webapp.access_to_pws_inspections') and obj.site.pws == request.user.employee.pws


class HomeView(BaseTemplateView):
    template_name = "home.html"
    permission = 'webapp.browse_site'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(HomeView, self).get_context_data(**kwargs)
        sites = self._get_sites_for_user(user)
        site_filter = SiteFilter(self.request.GET, queryset=sites)
        context['site_filter'] = site_filter
        return context

    def _get_sites_for_user(self, user):
        sites = []
        if user.has_perm('webapp.access_to_test_sites'):
            permissions = models.TestPermission.objects.filter(given_to=user, is_active=True)
            sites = self._filter_sites_by_related(permissions)
        if user.has_perm('webapp.access_to_survey_sites'):
            inspections = models.Inspection.objects.filter(assigned_to=user, is_active=True)
            sites = self._filter_sites_by_related(inspections)
        if user.has_perm('webapp.access_to_pws_sites'):
            sites = models.Site.objects.filter(pws=user.employee.pws)
        if user.has_perm('webapp.access_to_all_sites'):
            sites = models.Site.objects.all()
        return sites

    @staticmethod
    def _filter_sites_by_related(related):
        site_pks = [obj.site.pk for obj in related]
        return models.Site.objects.filter(pk__in=site_pks)


class SiteDetailView(BaseTemplateView, SiteObjectPermissionMixin):
    template_name = 'site.html'
    permission = 'webapp.browse_site'

    def get_context_data(self, **kwargs):
        context = super(SiteDetailView, self).get_context_data(**kwargs)
        context['site'] = models.Site.objects.get(pk=self.kwargs['pk'])
        if not self.has_perm(self.request, context['site']):
            raise Http404
        return context


class SiteBaseFormView(BaseFormView):
    template_name = 'site_form.html'
    form_class = forms.SiteForm
    model = models.Site

    def get_context_data(self, **kwargs):
        context = super(SiteBaseFormView, self).get_context_data(**kwargs)
        customers = models.Customer.objects.all()
        customer_filter = CustomerFilter(self.request.GET, queryset=customers)
        context['customer_filter'] = customer_filter
        return context

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


class SiteEditView(SiteBaseFormView, UpdateView, SiteObjectPermissionMixin):
    permission = 'webapp.change_site'
    success_message = Messages.Site.editing_success
    error_message = Messages.Site.editing_error

    def get_form(self, form_class):
        site = self.model.objects.get(pk=self.kwargs['pk'])
        if not self.has_perm(self.request, site):
            raise Http404
        form = super(SiteEditView, self).get_form(form_class)
        form.initial['customer'] = site.customer.pk
        return form


class PWSView(BaseTemplateView):
    template_name = 'pws_list.html'
    permission = 'webapp.browse_pws'

    def get_context_data(self, **kwargs):
        context = super(PWSView, self).get_context_data(**kwargs)
        context['pws_list'] = models.PWS.objects.all()
        return context


class PWSBaseFormView(BaseFormView):
    template_name = 'pws_form.html'
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


class CustomerView(BaseTemplateView):
    template_name = 'customer_base.html'
    permission = 'webapp.browse_customer'

    def get_context_data(self, **kwargs):
        context = super(CustomerView, self).get_context_data(**kwargs)
        customers = models.Customer.objects.all()
        customer_filter = CustomerFilter(self.request.GET, queryset=customers)
        context['customer_filter'] = customer_filter
        return context


class CustomerDetailView(BaseTemplateView):
    template_name = 'customer.html'
    permission = 'webapp.browse_customer'

    def get_context_data(self, **kwargs):
        context = super(CustomerDetailView, self).get_context_data(**kwargs)
        context['customer'] = models.Customer.objects.get(pk=self.kwargs['pk'])
        return context


class CustomerBaseFormView(BaseFormView):
    template_name = 'customer_form.html'
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


class SurveyDetailView(BaseTemplateView, SurveyObjectPermissionMixin):
    template_name = 'survey.html'
    permission = 'webapp.browse_survey'

    def get_context_data(self, **kwargs):
        context = super(SurveyDetailView, self).get_context_data(**kwargs)
        context['survey'] = models.Survey.objects.get(pk=self.kwargs['pk'])
        if not self.has_perm(self.request, context['survey']):
            raise Http404
        return context


class SurveyBaseFormView(BaseFormView):
    template_name = 'survey_form.html'
    form_class = forms.SurveyForm
    model = models.Survey

    def get_form(self, form_class):
        form = super(SurveyBaseFormView, self).get_form(form_class)
        if self.request.user.has_perm('webapp.access_to_own_surveys'):
            form.fields['surveyor'].queryset = models.User.objects.filter(pk=self.request.user.pk)
        if self.request.user.has_perm('webapp.access_to_pws_surveys'):
            form.fields['surveyor'].queryset = models.User.objects.filter(groups__name=Groups.surveyor,
                                                                          employee__pws=self.request.user.employee.pws)
        if self.request.user.has_perm('webapp.access_to_all_surveys'):
            form.fields['surveyor'].queryset = models.User.objects.filter(groups__name=Groups.surveyor)
        return form

    def get_success_url(self):
        return reverse('webapp:survey_detail', args=(self.object.pk,))


class SurveyAddView(SurveyBaseFormView, CreateView):
    permission = 'webapp.add_survey'

    def get_context_data(self, **kwargs):
        context = super(SurveyAddView, self).get_context_data(**kwargs)
        context['site_pk'] = self.kwargs['pk']
        return context

    def form_valid(self, form):
        form.instance.site = models.Site.objects.get(pk=self.kwargs['pk'])
        if not SiteObjectPermissionMixin.has_perm(self.request, form.instance.site):
            raise Http404
        form.instance.service_type = models.ServiceType.objects.filter(
            service_type__icontains=self.kwargs['service']
        )[0]
        return super(SurveyAddView, self).form_valid(form)


class SurveyEditView(SurveyBaseFormView, UpdateView, SurveyObjectPermissionMixin):
    permission = 'webapp.add_survey'

    def get_form(self, form_class):
        survey = self.model.objects.get(pk=self.kwargs['pk'])
        if not self.has_perm(self.request, survey):
            raise Http404
        return super(SurveyEditView, self).get_form(form_class)


class HazardDetailView(BaseTemplateView, HazardObjectPermissionMixin):
    template_name = 'hazard.html'
    permission = 'webapp.browse_hazard'

    def get_context_data(self, **kwargs):
        context = super(HazardDetailView, self).get_context_data(**kwargs)
        context['hazard'] = models.Hazard.objects.get(pk=self.kwargs['pk'])
        if not self.has_perm(self.request, context['hazard']):
            raise Http404
        tests_count = models.Test.objects.filter(bp_device=context['hazard'], tester=self.request.user).count()
        context['countlte0'] = tests_count <= 0
        return context


class HazardBaseFormView(BaseFormView):
    template_name = 'hazard_form.html'
    form_class = forms.HazardForm
    model = models.Hazard

    def get_success_url(self):
        return reverse('webapp:hazard_detail', args=(self.object.pk,))


class HazardAddView(HazardBaseFormView, CreateView):
    permission = 'webapp.add_hazard'
    success_message = Messages.Hazard.adding_success
    error = Messages.Hazard.adding_error

    def get_context_data(self, **kwargs):
        context = super(HazardAddView, self).get_context_data(**kwargs)
        context['survey_pk'] = self.kwargs['pk']
        return context

    def form_valid(self, form):
        form.instance.survey = models.Survey.objects.get(pk=self.kwargs['pk'])
        if not SurveyObjectPermissionMixin.has_perm(self.request, form.instance.survey):
            raise Http404
        return super(HazardAddView, self).form_valid(form)


class HazardEditView(HazardBaseFormView, UpdateView, HazardObjectPermissionMixin):
    permission = 'webapp.change_hazard'
    success_message = Messages.Hazard.editing_success
    error_message = Messages.Hazard.editing_error

    def form_invalid(self, form):
        print form.fields
        return super(HazardEditView, self).form_invalid(form)

    def get_form(self, form_class):
        hazard = self.model.objects.get(pk=self.kwargs['pk'])
        if not self.has_perm(self.request, hazard):
            raise Http404
        # Seems that it does not work, excluded fields appears in template anyway
        self.form_class.Meta.exclude = ['survey']
        if not self.request.user.has_perm('webapp.change_all_info_about_hazard'):
            self.form_class.Meta.exclude.extend(
                ['location1', 'location2', 'hazard_type', 'due_install_test_date', 'notes'])
        form = super(HazardEditView, self).get_form(form_class)
        if not self.request.user.has_perm('webapp.change_all_info_about_hazard'):
            form.fields['assembly_status'].queryset = models.AssemblyStatus.objects.filter(
                assembly_status__in=TESTER_ASSEMBLY_STATUSES)
        return form


class TestBaseFormView(BaseFormView):
    template_name = 'test_form.html'
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
        if self.request.user.has_perm('webapp.access_to_own_tests'):
            form.fields['tester'].queryset = models.User.objects.filter(pk=self.request.user.pk)
        if self.request.user.has_perm('webapp.access_to_pws_tests'):
            form.fields['tester'].queryset = models.User.objects.filter(groups__name=Groups.tester,
                                                                        employee__pws=self.request.user.employee.pws)
        if self.request.user.has_perm('webapp.access_to_all_tests'):
            form.fields['tester'].queryset = models.User.objects.filter(groups__name=Groups.tester)
        return form


class TestAddView(TestBaseFormView, CreateView):
    permission = 'webapp.add_test'
    success_message = Messages.Test.adding_success
    error_message = Messages.Test.adding_error

    def form_valid(self, form):
        form.instance.bp_device = models.Hazard.objects.get(pk=self.kwargs['pk'])
        if not HazardObjectPermissionMixin.has_perm(self.request, form.instance.bp_device):
            raise Http404
        return super(TestAddView, self).form_valid(form)


class TestEditView(TestBaseFormView, UpdateView):
    permission = 'webapp.edit_test'
    success_message = Messages.Test.editing_success
    error_message = Messages.Test.editing_error


class InspectionView(BaseTemplateView):
    permission = 'webapp.browse_inspection'
    template_name = 'inspection_list.html'

    def get_context_data(self, **kwargs):
        context = super(InspectionView, self).get_context_data(**kwargs)
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
    template_name = 'inspection_form.html'

    def get_success_url(self):
        return reverse('webapp:inspection_list')

    def get_form(self, form_class):
        form = super(InspectionBaseFormView, self).get_form(form_class)
        if self.request.user.has_perm('webapp.access_to_pws_inspections'):
            form.fields['assigned_to'].queryset = models.User.objects.filter(groups__name=Groups.surveyor, employee__pws=self.request.user.employee.pws)
        if self.request.user.has_perm('webapp.access_to_all_inspections'):
            form.fields['assigned_to'].queryset = models.User.objects.filter(groups__name=Groups.surveyor)
        return form


class InspectionAddView(InspectionBaseFormView, CreateView):
    permission = 'webapp.add_inspection'
    success_message = Messages.Inspection.adding_success
    error_message = Messages.Inspection.adding_error

    def form_valid(self, form):
        form.instance.assigned_by = self.request.user
        form.instance.site = models.Site.objects.get(pk=self.kwargs['pk'])
        return super(InspectionAddView, self).form_valid(form)


class InspectionEditView(InspectionBaseFormView, UpdateView):
    permission = 'webapp.change_permission'
    success_message = Messages.Inspection.editing_success
    error_message = Messages.Inspection.editing_error