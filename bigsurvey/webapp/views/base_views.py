from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import View, FormView, TemplateView, CreateView
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect, HttpResponse
from main.parameters import Messages, TEST_PRICE
from webapp import models
from webapp import forms
from django.utils.translation import ugettext as _


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

    def get(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            return super(HelpView, self).get(request, *args, **kwargs)
        available_help_items = models.StaticText.objects.filter(
            group=self.request.user.groups.all().first(),
            pdf_file__isnull=False
        ).order_by('-pk')
        if available_help_items:
            return HttpResponseRedirect(available_help_items.first().pdf_file.url, content_type='application/pdf')
        return Http404

    def get_context_data(self, **kwargs):
        context = super(HelpView, self).get_context_data(**kwargs)
        help_groups = [(_('Without Group'), models.StaticText.objects.filter(group=None, pdf_file__isnull=False))]
        for group in models.Group.objects.all():
            help_groups.append((group.name, models.StaticText.objects.filter(group=group, pdf_file__isnull=False)))
        context['help_groups'] = help_groups
        return context


class TestPriceSetupView(BaseFormView, CreateView):
    template_name = 'price_setup.html'
    model = models.PriceHistory
    form_class = forms.TestPriceForm
    permission = 'webapp.setup_test_price'
    success_url = reverse_lazy('webapp:test_price')

    def get_context_data(self, **kwargs):
        context = super(TestPriceSetupView, self).get_context_data(**kwargs)
        context['active_prices'] = models.PriceHistory.objects.filter(
                price_type=TEST_PRICE,end_date__isnull=True
            ).order_by('-start_date')
        context['old_prices'] = models.PriceHistory.objects.filter(
            price_type=TEST_PRICE
        ).exclude(end_date__isnull=True).order_by('-start_date')
        return context

    def form_valid(self, form):
        pws_multiple=form.cleaned_data.get('pws_multiple')
        if not pws_multiple:
            current_price = models.PriceHistory.current_for_test()
            if current_price:
                current_date = datetime.now().date()
                if current_date == current_price.start_date:
                    current_price.price = form.cleaned_data['price']
                else:
                    form.instance.price_type = TEST_PRICE
                    self.object = form.save()
                    current_price.end_date = self.object.start_date
                current_price.save()
            else:
                form.instance.price_type = TEST_PRICE
                self.object = form.save()
        else:
            for pws in pws_multiple:
                current_price = models.PriceHistory.current_for_test(pws)
                if current_price:
                    current_date = datetime.now().date()
                    if current_date == current_price.start_date:
                        current_price.price = form.cleaned_data['price']
                    else:
                        form.instance.price_type = TEST_PRICE
                        self.object = form.save(commit=False)
                        self.object.pws=pws
                        new_price=models.PriceHistory()
                        new_price.save_multiple(self.object)
                        current_price.end_date = self.object.start_date
                    current_price.save()
                else:
                    form.instance.price_type = TEST_PRICE
                    self.object = form.save(commit=False)
                    self.object.pws=pws
                    new_price = models.PriceHistory()
                    new_price.save_multiple(self.object)
        return HttpResponseRedirect(self.success_url)
