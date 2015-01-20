from django.views.generic import TemplateView, View
import models
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from filters import SiteFilter


class LoginRequiredView(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredView, self).dispatch(*args, **kwargs)


class HomeView(TemplateView, LoginRequiredView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data()
        user = self.request.user
        user_groups = user.groups.values_list('name', flat=True)
        if "SuperAdministrators" in user_groups:
            context['admin'] = True
            context['super'] = True
            sites = models.Site.objects.all()
        elif "Administrators" in user_groups:
            if user.licences.filter(is_active=True).exists():
                context['admin'] = True
                sites = models.Site.objects.filter(pws=user.employee.pws)
        elif "Surveyors" in user_groups:
            context['surv'] = True
            inspections = models.Inspection.objects.filter(assigned_to=user, is_active=True)
            site_pks = []
            for inspection in inspections:
                site_pks.append(inspection.site.pk)
            sites = models.Site.objects.filter(pk__in=site_pks)
        elif "Testers" in user_groups:
            context['test'] = True
            permissions = models.TestPermission.objects.filter(given_to=user, is_active=True)
            site_pks = []
            for permission in permissions:
                site_pks.append(permission.site.pk)
            sites = models.Site.objects.filter(pk__in=site_pks)
        site_filter = SiteFilter(self.request.GET, queryset=sites)
        context['site_filter'] = site_filter
        return context