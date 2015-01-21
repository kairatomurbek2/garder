from django.views.generic import TemplateView, View, CreateView, UpdateView
import models
import forms
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from filters import SiteFilter
from django.http import Http404
from django.core.urlresolvers import reverse


class BaseView(View):
    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        user = self.request.user
        user_groups = user.groups.values_list('name', flat=True)
        if "SuperAdministrators" in user_groups:
            context['admin'] = True
            context['super'] = True
        elif "Administrators" in user_groups:
            context['admin'] = True
        elif "Surveyors" in user_groups:
            context['surv'] = True
        elif "Testers" in user_groups:
            context['test'] = True
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BaseView, self).dispatch(*args, **kwargs)


class BaseTemplateView(BaseView, TemplateView):
    pass


class SuperAdministratorView(BaseView):
    def get_context_data(self, **kwargs):
        context = super(SuperAdministratorView, self).get_context_data(**kwargs)
        if not context.get('super'):
            raise Http404
        return context


class HomeView(BaseTemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(HomeView, self).get_context_data(**kwargs)
        if context.get('super'):
            sites = models.Site.objects.all()
        elif context.get('admin'):
            sites = models.Site.objects.filter(pws=user.employee.pws)
        elif context.get('surv'):
            inspections = models.Inspection.objects.filter(assigned_to=user, is_active=True)
            sites = self.filter_sites_by_related(inspections)
        elif context.get('test'):
            permissions = models.TestPermission.objects.filter(given_to=user, is_active=True)
            sites = self.filter_sites_by_related(permissions)
        site_filter = SiteFilter(self.request.GET, queryset=sites)
        context['site_filter'] = site_filter
        return context

    def filter_sites_by_related(self, related):
        site_pks = []
        for obj in related:
            site_pks.append(obj.site.pk)
        return models.Site.objects.filter(pk__in=site_pks)


class SiteDetailView(BaseTemplateView):
    template_name = 'site.html'

    def get_context_data(self, **kwargs):
        context = super(SiteDetailView, self).get_context_data(**kwargs)
        context['site'] = models.Site.objects.get(pk=self.kwargs['pk'])
        return context


class PWSView(BaseTemplateView):
    template_name = 'pws_list.html'

    def get_context_data(self, **kwargs):
        context = super(PWSView, self).get_context_data(**kwargs)
        context['pws_list'] = models.PWS.objects.all()
        return context


class PWSAddView(CreateView, SuperAdministratorView):
    template_name = 'pws_form.html'
    form_class = forms.PWSForm
    model = models.PWS

    def get_success_url(self):
        return reverse('webapp:pws_list')


class PWSEditView(UpdateView, SuperAdministratorView):
    template_name = 'pws_form.html'
    form_class = forms.PWSForm
    model = models.PWS

    def get_success_url(self):
        return reverse('webapp:pws_list')