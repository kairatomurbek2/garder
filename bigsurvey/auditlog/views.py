from django.views.generic import FormView

from webapp import models
from webapp.views import BaseTemplateView
from . import forms
from .auditlog_helpers import get_version_objects_with_diff


class AuditLogView(BaseTemplateView, FormView):
    template_name = 'auditlog/auditlog.html'
    permission = 'webapp.access_to_audit_log'
    form_class = forms.AuditLogFilterForm

    def get_context_data(self, **kwargs):
        context = super(AuditLogView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.has_perm('webapp.browse_all_pws'):
            pws_list = models.PWS.objects.all()
        elif self.request.user.has_perm('webapp.own_multiple_pws'):
            pws_list = user.employee.pws.all()
        else:
            pws_list = models.PWS.objects.none()
        form = self.form_class(self.request.GET or None)
        form.fields['pws'].queryset = pws_list
        if self.request.GET and set(form.fields.keys()).issubset(set(self.request.GET.keys())):
            if form.is_valid():
                context['form'] = form
                context['version_objects_with_diffs'] = get_version_objects_with_diff(form, pws_list)
        context['form'] = form
        return context
