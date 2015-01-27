from django.views.generic import TemplateView, View, CreateView, UpdateView
import models
import forms
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from filters import SiteFilter
from django.http import Http404
from django.core.urlresolvers import reverse


class BaseView(TemplateView):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BaseView, self).dispatch(*args, **kwargs)


class SuperAdministratorView(BaseView):
    def get_context_data(self, **kwargs):
        if not self.request.user.is_superadmin:
            raise Http404
        return super(SuperAdministratorView, self).get_context_data(**kwargs)


class HomeView(BaseView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(HomeView, self).get_context_data(**kwargs)
        sites = []
        if user.has_perm('webapp.can_see_test_sites'):
            permissions = models.TestPermission.objects.filter(given_to=user, is_active=True)
            sites = self.filter_sites_by_related(permissions)
        if user.has_perm('webapp.can_see_surv_sites'):
            inspections = models.Inspection.objects.filter(assigned_to=user, is_active=True)
            sites = self.filter_sites_by_related(inspections)
        if user.has_perm('webapp.can_see_pws_sites'):
            sites = models.Site.objects.filter(pws=user.employee.pws)
        if user.has_perm('webapp.can_see_all_sites'):
            sites = models.Site.objects.all()
        site_filter = SiteFilter(self.request.GET, queryset=sites)
        context['site_filter'] = site_filter
        return context

    def filter_sites_by_related(self, related):
        site_pks = []
        for obj in related:
            site_pks.append(obj.site.pk)
        return models.Site.objects.filter(pk__in=site_pks)


class SiteDetailView(BaseView):
    template_name = 'site.html'

    def get_context_data(self, **kwargs):
        context = super(SiteDetailView, self).get_context_data(**kwargs)
        context['site'] = models.Site.objects.get(pk=self.kwargs['pk'])
        return context


class PWSAccessMixin(BaseView):
    def get_context_data(self, **kwargs):
        if not self.request.user.has_perm('webapp.has_access_to_pws'):
            raise Http404
        return super(PWSAccessMixin, self).get_context_data(**kwargs)


class PWSView(PWSAccessMixin):
    template_name = 'pws_list.html'

    def get_context_data(self, **kwargs):
        context = super(PWSView, self).get_context_data(**kwargs)
        context['pws_list'] = models.PWS.objects.all()
        return context


class PWSAddView(PWSAccessMixin):
    template_name = 'pws_form.html'
    form_class = forms.PWSForm
    model = models.PWS

    def get_success_url(self):
        return reverse('webapp:pws_list')


class PWSEditView(PWSAccessMixin):
    template_name = 'pws_form.html'
    form_class = forms.PWSForm
    model = models.PWS

    def get_success_url(self):
        return reverse('webapp:pws_list')