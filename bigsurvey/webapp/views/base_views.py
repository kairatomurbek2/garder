from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import View, FormView, TemplateView, CreateView
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from main.parameters import Messages
from webapp import models
from webapp import forms


class PermissionRequiredMixin(View):
    permission = None

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.permission and not self.request.user.has_perm(self.permission):
            raise Http404
        return super(PermissionRequiredMixin, self).dispatch(*args, **kwargs)


class BaseView(PermissionRequiredMixin):
    def has_more_link(self):
        user = self.request.user
        return user.has_perm('webapp.access_to_adminpanel') or \
               user.has_perm('webapp.browse_all_pws') or \
               user.has_perm('webapp.browse_lettertype') or \
               not user.is_superuser and user.has_perm('webapp.change_own_pws') and user.employee.pws or \
               user.has_perm('webapp.browse_user') or \
               user.has_perm('webapp.access_to_import') or \
               user.has_perm('webapp.browse_import_log') or \
               user.has_perm('webapp.access_to_batch_update')

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        context['has_more_link'] = self.has_more_link()
        return context


class BaseTemplateView(BaseView, TemplateView):
    pass


class BaseFormView(BaseView, FormView):
    success_message = None
    error_message = Messages.form_error

    def form_valid(self, form):
        if self.success_message:
            messages.success(self.request, self.success_message)
        return super(BaseFormView, self).form_valid(form)

    def form_invalid(self, form):
        if self.error_message:
            messages.error(self.request, self.error_message)
        return super(BaseFormView, self).form_invalid(form)


class HelpView(BaseTemplateView):
    template_name = 'help.html'

    def get_context_data(self, **kwargs):
        context = super(HelpView, self).get_context_data(**kwargs)
        context['user_help'] = models.StaticText.objects.filter(group__in=self.request.user.groups.all())
        context['for_all_help'] = models.StaticText.objects.filter(group=None)
        return context


class TestPriceSetupView(BaseFormView, CreateView):
    template_name = 'price_setup.html'
    model = models.TestPriceHistory
    form_class = forms.TestPriceForm
    permission = 'webapp.setup_price'
    success_url = reverse_lazy('webapp:test_price')

    def get_context_data(self, **kwargs):
        context = super(TestPriceSetupView, self).get_context_data(**kwargs)
        context['price_history'] = models.TestPriceHistory.objects.all().order_by('-start_date')
        return context

    def form_valid(self, form):
        current_price = models.TestPriceHistory.current()
        current_date = datetime.now().date()
        if current_date == current_price.start_date:
            current_price.price = form.cleaned_data['price']
        else:
            self.object = form.save()
            current_price.end_date = self.object.start_date
        current_price.save()
        return HttpResponseRedirect(self.success_url)
