from django.views.generic import TemplateView, View, CreateView, UpdateView
import models
import forms
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from filters import SiteFilter
from django.http import Http404
from django.core.urlresolvers import reverse
from abc import ABCMeta, abstractmethod
from django.contrib import messages
from main.parameters import Messages, Groups


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
               request.user.has_perm('webapp.access_to_survey_sites') and obj.inspections.filter(assigned_to=request.user) or \
               request.user.has_perm('webapp.access_to_test_sites') and obj.test_perms.filter(given_to=request.user)


class SurveyObjectPermissionMixin(ObjectPermissionMixin):
    @staticmethod
    def has_perm(request, obj):
        return request.user.has_perm('webapp.access_to_all_surveys') or \
               request.user.has_perm('webapp.access_to_pws_surveys') and obj.site.pws == request.user.employee.pws or \
               request.user.has_perm('webapp.access_to_own_surveys') and obj.surveyor == request.user


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


class SiteAddView(BaseView, CreateView):
    template_name = 'site_form.html'
    form_class = forms.SiteForm
    model = models.Site
    permission = 'webapp.add_site'

    def get_form(self, form_class):
        form = super(SiteAddView, self).get_form(form_class)
        if not self.request.user.has_perm('webapp.access_to_all_sites'):
            form.fields['pws'].queryset = models.PWS.objects.filter(pk=self.request.user.employee.pws.pk)
        return form

    def form_valid(self, form):
        messages.success(self.request, Messages.Site.adding_success)
        return super(SiteAddView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, Messages.Site.adding_error)
        return super(SiteAddView, self).form_invalid(form)

    def get_success_url(self):
        return reverse('webapp:home')


class SiteEditView(BaseView, UpdateView, SiteObjectPermissionMixin):
    template_name = 'site_form.html'
    form_class = forms.SiteForm
    model = models.Site
    permission = 'webapp.change_site'

    def get_context_data(self, **kwargs):
        site = models.Site.objects.get(pk=self.kwargs['pk'])
        if not self.has_perm(self.request, site):
            raise Http404
        return super(SiteEditView, self).get_context_data(**kwargs)

    def get_form(self, form_class):
        form = super(SiteEditView, self).get_form(form_class)
        if not self.request.user.has_perm('webapp.access_to_all_sites'):
            form.fields['pws'].queryset = models.PWS.objects.filter(pk=self.request.user.employee.pws.pk)
        return form

    def form_valid(self, form):
        messages.success(self.request, Messages.Site.editing_success)
        return super(SiteEditView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, Messages.Site.editing_error)
        return super(SiteEditView, self).form_invalid(form)

    def get_success_url(self):
        return reverse('webapp:home')


class PWSView(BaseTemplateView):
    template_name = 'pws_list.html'
    permission = 'webapp.browse_pws'

    def get_context_data(self, **kwargs):
        context = super(PWSView, self).get_context_data(**kwargs)
        context['pws_list'] = models.PWS.objects.all()
        return context


class PWSAddView(BaseView, CreateView):
    template_name = 'pws_form.html'
    form_class = forms.PWSForm
    model = models.PWS
    permission = 'webapp.add_pws'

    def get_success_url(self):
        return reverse('webapp:pws_list')

    def form_valid(self, form):
        messages.success(self.request, Messages.PWS.adding_success)
        return super(PWSAddView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, Messages.PWS.adding_error)
        return super(PWSAddView, self).form_invalid(form)


class PWSEditView(BaseView, UpdateView):
    template_name = 'pws_form.html'
    form_class = forms.PWSForm
    model = models.PWS
    permission = 'webapp.change_pws'

    def get_success_url(self):
        return reverse('webapp:pws_list')

    def form_valid(self, form):
        messages.success(self.request, Messages.PWS.editing_success)
        return super(PWSEditView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, Messages.PWS.editing_error)
        return super(PWSEditView, self).form_invalid(form)


class CustomerView(BaseTemplateView):
    template_name = 'customer_list.html'
    permission = 'webapp.browse_customer'

    def get_context_data(self, **kwargs):
        context = super(CustomerView, self).get_context_data(**kwargs)
        context['customer_list'] = models.Customer.objects.all()
        return context


class CustomerDetailView(BaseTemplateView):
    template_name = 'customer.html'
    permission = 'webapp.browse_customer'

    def get_context_data(self, **kwargs):
        context = super(CustomerDetailView, self).get_context_data(**kwargs)
        context['customer'] = models.Customer.objects.get(pk=self.kwargs['pk'])
        return context


class CustomerAddView(BaseView, CreateView):
    template_name = 'customer_form.html'
    form_class = forms.CustomerForm
    model = models.Customer
    permission = 'webapp.add_customer'

    def get_success_url(self):
        return reverse('webapp:customer_list')

    def form_valid(self, form):
        messages.success(self.request, Messages.Customer.adding_success)
        return super(CustomerAddView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, Messages.Customer.adding_error)
        return super(CustomerAddView, self).form_invalid(form)


class CustomerEditView(BaseView, UpdateView):
    template_name = 'customer_form.html'
    form_class = forms.CustomerForm
    model = models.Customer
    permission = 'webapp.change_customer'

    def get_success_url(self):
        return reverse('webapp:customer_list')

    def form_valid(self, form):
        messages.success(self.request, Messages.Customer.editing_success)
        return super(CustomerEditView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, Messages.Customer.editing_error)
        return super(CustomerEditView, self).form_invalid(form)


class SurveyDetailView(BaseTemplateView, SurveyObjectPermissionMixin):
    template_name = 'survey.html'
    permission = 'webapp.browse_survey'

    def get_context_data(self, **kwargs):
        context = super(SurveyDetailView, self).get_context_data(**kwargs)
        context['survey'] = models.Survey.objects.get(pk=self.kwargs['pk'])
        if not self.has_perm(self.request, context['survey']):
            raise Http404
        context['site'] = context['survey'].site
        return context


class SurveyAddView(BaseView, CreateView):
    template_name = 'survey_form.html'
    form_class = forms.SurveyForm
    model = models.Survey
    permission = 'webapp.add_survey'

    def get_success_url(self):
        return reverse('webapp:survey_detail', args=(self.kwargs['pk'],))

    def get_form(self, form_class):
        form = super(SurveyAddView, self).get_form(form_class)
        if self.request.user.has_perm('webapp.access_to_own_surveys'):
            form.fields['surveyor'].queryset = models.User.objects.filter(pk=self.request.user.pk)
        if self.request.user.has_perm('webapp.access_to_pws_surveys'):
            form.fields['surveyor'].queryset = models.User.objects.filter(groups__name=Groups.surveyor, employee__pws=self.request.user.employee.pws)
        if self.request.user.has_perm('webapp.access_to_all_surveys'):
            form.fields['surveyor'].queryset = models.User.objects.filter(groups__name=Groups.surveyor)
        return form

    def form_valid(self, form):
        form.instance.site = models.Site.objects.get(pk=self.kwargs['pk'])
        if not SiteObjectPermissionMixin.has_perm(self.request, form.instance.site):
            raise Http404
        form.instance.service_type = models.ServiceType.objects.get(pk=self.kwargs['service_type_pk'])
        return super(SurveyAddView, self).form_valid(form)

    def form_invalid(self, form):
        # messages.error(self.request, Messages.Customer.adding_error)
        return super(SurveyAddView, self).form_invalid(form)


class SurveyEditView(BaseView, UpdateView, SurveyObjectPermissionMixin):
    pass