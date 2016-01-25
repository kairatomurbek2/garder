import datetime

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.views.generic import FormView, CreateView, UpdateView
from main.parameters import SITE_STATUS, BP_TYPE, Messages
from webapp import filters, models, forms, perm_checkers
from webapp.actions.builders import SiteFilteringActionsBuilder
from webapp.models import NoSearchFieldIndicated
from webapp.utils.excel_writer import XLSExporter
from .base_views import BaseTemplateView, BaseFormView


class HomeView(FormView, BaseTemplateView):
    template_name = "home.html"
    permission = 'webapp.browse_site'
    form_class = forms.SitesFilterForm

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_superuser and user.has_perm('webapp.access_to_site_by_customer_account'):
            return redirect('webapp:tester-home')
        if 'xls' in self.request.GET:
            if user.has_perm('webapp.export_xls'):
                return self._get_xls()
        return super(HomeView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        sites = self._get_sites()
        pws_list = self._get_pws_list()
        if self.request.GET:
            form = self.form_class(self.request.GET, pws_qs=pws_list)
            if form.is_valid():
                action = SiteFilteringActionsBuilder.get_sites_filtered(form, pws_list, sites)
                context['site_filter_form'] = form
                context['sites'] = action.execute()
                return context
            else:
                context['site_filter_form'] = form
                return context
        context['site_filter_form'] = self.form_class(pws_qs=pws_list)
        context['sites'] = sites
        return context

    def _get_xls(self):
        pws_list = self._get_pws_list()
        form = self.form_class(self.request.GET, pws_qs=pws_list)
        if form.is_valid():
            action = SiteFilteringActionsBuilder.get_sites_filtered(form, pws_list, self._get_sites())
            filtered_sites = action.execute()
            xls = XLSExporter(filtered_sites).get_xls()
            response = HttpResponse(xls, content_type='text/plain')
            return response

    def _get_sites(self):
        sites = models.Site.objects.none()
        if self.request.user.has_perm('webapp.access_to_pws_sites'):
            sites = models.Site.objects.filter(pws__in=self.request.user.employee.pws.all())
        if self.request.user.has_perm('webapp.access_to_all_sites'):
            sites = models.Site.objects.all()
        return sites.filter(status__site_status__iexact=SITE_STATUS.ACTIVE)

    def _get_pws_list(self):
        pws_list = models.PWS.objects.none()
        if self.request.user.has_perm('webapp.browse_all_pws'):
            pws_list = models.PWS.objects.all()
        elif self.request.user.has_perm('webapp.own_multiple_pws'):
            pws_list = self.request.user.employee.pws.all()
        return pws_list


class TesterHomeView(BaseTemplateView, FormView):
    template_name = 'tester_home.html'
    permission = 'webapp.access_to_site_by_customer_account'
    form_class = forms.TesterSiteSearchForm

    def get_context_data(self, **kwargs):
        context = super(TesterHomeView, self).get_context_data(**kwargs)
        form = self.form_class(self.request.GET or None)
        pws = self.request.user.employee.pws.all()
        form.fields['pws'].queryset = pws
        if self.request.GET and set(form.fields.keys()).issubset(set(self.request.GET.keys())):
            if form.is_valid():
                search_field = form.search_field_and_value.keys()[0]
                search_value = form.search_field_and_value.get(search_field)
                context['form'] = form
                context['search_field'] = form.fields[search_field].label
                context['search_value'] = search_value
                try:
                    search_results = models.Site.search_in_cust_number_address_meter_number(
                        pws, search_field, search_value)
                except NoSearchFieldIndicated:
                    search_results = []
                    messages.error(self.request, Messages.Site.search_server_error)
                context['sites_queryset'] = search_results
                self.request.session['sites_pks'] = [site.pk for site in search_results]
        context['form'] = form
        return context


class SiteDetailView(BaseTemplateView):
    template_name = 'site/site.html'
    permission = 'webapp.browse_site'

    def get_context_data(self, **kwargs):
        site = models.Site.objects.get(pk=self.kwargs['pk'])
        if not perm_checkers.SitePermChecker.has_perm(self.request, site):
            raise Http404
        context = super(SiteDetailView, self).get_context_data(**kwargs)
        context['site'] = site
        context['BP_TYPE'] = BP_TYPE
        return context


class SiteBaseFormView(BaseFormView):
    template_name = 'site/site_form.html'
    form_class = forms.SiteForm
    form_class_for_surveyor = forms.SiteFormForSurveyor
    model = models.Site

    def get_form_class(self):
        if self.request.user.has_perm('webapp.change_all_info_about_site'):
            return self.form_class
        return self.form_class_for_surveyor

    def get_form(self, form_class):
        form = super(SiteBaseFormView, self).get_form(form_class)
        if self.request.user.has_perm('webapp.change_all_info_about_site'):
            if not self.request.user.has_perm('webapp.access_to_all_sites'):
                form.fields['pws'].queryset = self.request.user.employee.pws.all()
        return form

    def get_success_url(self):
        return reverse('webapp:site_detail', args=(self.object.pk,))


class SiteAddView(SiteBaseFormView, CreateView):
    permission = 'webapp.add_site'
    success_message = Messages.Site.adding_success
    error_message = Messages.Site.adding_error

    def form_invalid(self, form):
        cust_number = form.cleaned_data.get('cust_number')
        pws = form.cleaned_data.get('pws')
        if cust_number in [site.cust_number for site in pws.sites.all()]:
            form.add_error('cust_number', ValidationError(Messages.Site.account_number_exists))
        return super(SiteAddView, self).form_invalid(form)


class SiteEditView(SiteBaseFormView, UpdateView):
    permission = 'webapp.change_site'
    success_message = Messages.Site.editing_success
    error_message = Messages.Site.editing_error

    def get_form(self, form_class):
        form = super(SiteEditView, self).get_form(form_class)
        if not perm_checkers.SitePermChecker.has_perm(self.request, form.instance):
            raise Http404
        return form


class BatchUpdateView(BaseTemplateView):
    template_name = 'site/site_batch_update.html'
    permission = 'webapp.access_to_batch_update'
    filter_class = filters.SiteFilter
    form_class = forms.BatchUpdateForm

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(BatchUpdateView, self).get_context_data(**kwargs)
        sites = self._get_sites(user)
        context['site_filter'] = self._get_site_filter(queryset=sites)
        context['form'] = self.form_class()
        return context

    @staticmethod
    def _get_sites(user):
        sites = models.Site.objects.none()
        if user.has_perm('webapp.access_to_pws_sites'):
            sites = models.Site.objects.filter(pws__in=user.employee.pws.all())
        if user.has_perm('webapp.access_to_all_sites'):
            sites = models.Site.objects.all()
        return sites

    def _get_site_filter(self, queryset):
        return self.filter_class(self.request.GET, queryset=queryset)

    def post(self, request):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            empty = form.cleaned_data.get('empty_date')
            site_pks = self.request.POST.getlist('site_pks')
            if empty:
                self._batch_update(None, site_pks)
                messages.success(self.request, Messages.BatchUpdate.success)
            else:
                date = form.cleaned_data.get('date')
                if date:
                    self._batch_update(date, site_pks)
                    messages.success(self.request, Messages.BatchUpdate.success)
                else:
                    messages.error(self.request, Messages.BatchUpdate.error)
        else:
            messages.error(self.request, Messages.BatchUpdate.error)
        return redirect(self.get_success_url())

    def _batch_update(self, date, site_pks):
        if 'set_sites_next_survey_date' in self.request.POST:
            self._batch_update_sites(date, site_pks)
        elif 'set_sites_last_survey_date' in self.request.POST:
            if date and date > datetime.date.today():
                messages.error(self.request, Messages.BatchUpdate.error_date_in_future)
            else:
                self._batch_update_survey(date, site_pks)
        else:
            self._batch_update_hazards(date, site_pks)

    def _batch_update_sites(self, date, site_pks):
        models.Site.objects.filter(pk__in=site_pks).update(next_survey_date=date)

    def _batch_update_hazards(self, date, site_pks):
        models.Site.objects.filter(pk__in=site_pks).update(due_install_test_date=date)

    def _batch_update_survey(self, date, site_pks):
        models.Site.objects.filter(pk__in=site_pks).update(last_survey_date=date)

    def get_success_url(self):
        return reverse('webapp:batch_update')
