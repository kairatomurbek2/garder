from django.views.generic import TemplateView, View, CreateView, UpdateView
import models
import forms
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from filters import SiteFilter
from django.http import Http404
from django.core.urlresolvers import reverse
from abc import ABCMeta, abstractmethod


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


class ObjectMixin(object):
    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def has_perm(request, obj):
        pass


class SiteObjectMixin(ObjectMixin):
    @staticmethod
    def has_perm(request, obj):
        return request.user.has_perm('webapp.browse_all_sites') or \
               obj.pws == request.user.employee.pws or \
               obj.inspections.filter(assigned_to=request.user) or \
               obj.test_perms.filter(given_to=request.user)


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
        if user.has_perm('webapp.browse_site'):
            if user.has_perm('webapp.browse_test_sites'):
                permissions = models.TestPermission.objects.filter(given_to=user, is_active=True)
                sites = self._filter_sites_by_related(permissions)
            if user.has_perm('webapp.browse_surv_sites'):
                inspections = models.Inspection.objects.filter(assigned_to=user, is_active=True)
                sites = self._filter_sites_by_related(inspections)
            if user.has_perm('webapp.browse_pws_sites'):
                sites = models.Site.objects.filter(pws=user.employee.pws)
            if user.has_perm('webapp.browse_all_sites'):
                sites = models.Site.objects.all()
        return sites

    @staticmethod
    def _filter_sites_by_related(related):
        site_pks = []
        for obj in related:
            site_pks.append(obj.site.pk)
        return models.Site.objects.filter(pk__in=site_pks)


class SiteDetailView(BaseTemplateView, SiteObjectMixin):
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
        if not self.request.user.has_perm('webapp.browse_all_sites'):
            form.fields['pws'].queryset = models.PWS.objects.filter(pk=self.request.user.employee.pws.pk)
        return form

    def get_success_url(self):
        return reverse('webapp:home')


class SiteEditView(BaseView, UpdateView, SiteObjectMixin):
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
        if not self.request.user.has_perm('webapp.browse_all_sites'):
            form.fields['pws'].queryset = models.PWS.objects.filter(pk=self.request.user.employee.pws.pk)
        return form

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


class PWSEditView(BaseView, UpdateView):
    template_name = 'pws_form.html'
    form_class = forms.PWSForm
    model = models.PWS
    permission = 'webapp.change_pws'

    def get_success_url(self):
        return reverse('webapp:pws_list')


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


class CustomerAddView(CreateView):
    template_name = 'customer_form.html'
    form_class = forms.CustomerForm
    model = models.Customer

    def get_success_url(self):
        return reverse('webapp:customer_list')


class CustomerEditView(UpdateView):
    template_name = 'customer_form.html'
    form_class = forms.CustomerForm
    model = models.Customer

    def get_success_url(self):
        return reverse('webapp:customer_list')