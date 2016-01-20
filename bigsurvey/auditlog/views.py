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
                context['version_objects_with_diffs'] = get_version_objects_with_diff(
                    pws_list, **self._prepare_kwargs(form))
                return context
            else:
                context['form'] = form
                return context
        context['form'] = form
        context['version_objects_with_diffs'] = get_version_objects_with_diff(pws_list, **self._prepare_kwargs(form))
        return context

    @staticmethod
    def _prepare_kwargs(form):
        kwargs = {}
        try:
            kwargs['start_date'] = form.cleaned_data['start_date']
            kwargs['end_date'] = form.cleaned_data['end_date']
            kwargs['pws'] = form.cleaned_data['pws']
            kwargs['user_group'] = form.cleaned_data['user_group']
            kwargs['username'] = form.cleaned_data['username']
            kwargs['record_object'] = form.cleaned_data['record_object']
        except AttributeError:
            kwargs['start_date'] = form.first_day_of_cur_month
            kwargs['end_date'] = form.last_day_of_cur_month
            kwargs['pws'] = None
            kwargs['user_group'] = None
            kwargs['username'] = ''
            kwargs['record_object'] = ''
        return kwargs
