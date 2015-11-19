from .base_views import BaseTemplateView, BaseFormView
from django.http import Http404
from django.core.urlresolvers import reverse
from webapp import models, forms
from main.parameters import Messages
from django.views.generic import UpdateView, CreateView


class PWSListView(BaseTemplateView):
    template_name = 'pws/pws_list.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(PWSListView, self).get_context_data(**kwargs)
        if user.has_perm('webapp.browse_all_pws'):
            pws_list = models.PWS.objects.all()
        elif user.has_perm('webapp.own_multiple_pws'):
            pws_list = user.employee.pws.all()
        else:
            raise Http404
        context['pws_list'] = pws_list
        return context


class PWSDetailView(BaseTemplateView):
    template_name = 'pws/pws.html'
    permission = 'webapp.browse_pws'

    def get_context_data(self, **kwargs):
        context = super(PWSDetailView, self).get_context_data(**kwargs)
        pws = models.PWS.objects.get(pk=self.kwargs['pk'])
        user = self.request.user
        if not user.is_superuser and user.has_perm('webapp.change_own_pws') and pws not in user.employee.pws.all():
            raise Http404
        context['pws'] = pws
        return context


class PWSBaseFormView(BaseFormView):
    template_name = 'pws/pws_form.html'
    form_class = forms.PWSForm
    model = models.PWS

    def get_success_url(self):
        return reverse('webapp:pws_detail', args=(self.object.pk,))


class PWSAddView(PWSBaseFormView, CreateView):
    permission = 'webapp.add_pws'
    success_message = Messages.PWS.adding_success
    error_message = Messages.PWS.adding_error

    def form_valid(self, form):
        form_is_valid = super(PWSAddView, self).form_valid(form)
        user = self.request.user
        if user.has_perm('webapp.own_multiple_pws'):
            user.employee.pws.add(self.object)
            user.employee.save()
        return form_is_valid


class PWSEditView(PWSBaseFormView, UpdateView):
    permission = 'webapp.change_pws'
    success_message = Messages.PWS.editing_success
    error_message = Messages.PWS.editing_error
    form_class_for_admin = forms.PWSFormForAdmin

    def get_form_class(self):
        user = self.request.user
        if not user.is_superuser and user.has_perm('webapp.change_own_pws'):
            return self.form_class_for_admin
        return self.form_class

    def get_context_data(self, **kwargs):
        user = self.request.user
        if not user.is_superuser and user.has_perm('webapp.change_own_pws') and self.object not in user.employee.pws.all():
            raise Http404
        return super(PWSEditView, self).get_context_data(**kwargs)
