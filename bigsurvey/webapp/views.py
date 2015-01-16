from django.views.generic import TemplateView, View
import models
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


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
            context['site_list'] = models.Site.objects.all()
        elif "Administrators" in user_groups:
            if user.licences.filter(is_active=True).exists():
                context['admin'] = True
                context['site_list'] = models.Site.objects.filter(pws=user.employee.pws)
        elif "Surveyors" in user_groups:
            context['surv'] = True
            inspections = models.Inspection.objects.filter(assigned_to=user)
            sites = []
            for inspection in inspections:
                sites.append(inspection.site)
            context['site_list'] = sites
        elif "Testers" in user_groups:
            context['test'] = True
            permissions = models.TestPermission.objects.filter(given_to=user)
            sites = []
            for permission in permissions:
                sites.append(permission.site)
            context['site_list'] = sites
        return context