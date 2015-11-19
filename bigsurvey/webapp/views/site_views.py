from .base_views import BaseTemplateView, BaseFormView
from webapp.utils.excel_writer import XLSExporter
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from webapp import filters, models, forms, perm_checkers
from django.views.generic import FormView, CreateView, UpdateView
from main.parameters import SITE_STATUS, BP_TYPE, Messages
from django.contrib import messages


class HomeView(BaseTemplateView):
    template_name = "home.html"
    permission = 'webapp.browse_site'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_superuser and user.has_perm('webapp.access_to_site_by_customer_account'):
            return redirect('webapp:tester-home')
        if 'xls' in self.request.GET:
            if user.has_perm('webapp.export_xls'):
                return self._get_xls()
        return super(HomeView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(HomeView, self).get_context_data(**kwargs)
        sites = self._get_sites(user)
        context['site_filter'] = filters.SiteFilter(self.request.GET, queryset=sites)
        return context

    def _get_xls(self):
        filtered_sites = filters.SiteFilter(self.request.GET, queryset=self._get_sites(self.request.user))
        xls = XLSExporter(filtered_sites.qs).get_xls()
        response = HttpResponse(xls, content_type='text/plain')
        return response

    def _get_sites(self, user):
        sites = models.Site.objects.none()
        if user.has_perm('webapp.access_to_pws_sites'):
            sites = models.Site.objects.filter(pws__in=user.employee.pws.all())
        if user.has_perm('webapp.access_to_all_sites'):
            sites = models.Site.objects.all()
        return sites.filter(status__site_status__iexact=SITE_STATUS.ACTIVE)


class TesterHomeView(BaseTemplateView, FormView):
    template_name = 'tester_home.html'
    permission = 'webapp.access_to_site_by_customer_account'
    form_class = forms.TesterSiteSearchForm

    def get_context_data(self, **kwargs):
        context = super(TesterHomeView, self).get_context_data(**kwargs)
        form = self.form_class(self.request.POST or None)
        form.fields['pws'].queryset = self.request.user.employee.pws.all()
        context['form'] = form
        return context

    def form_valid(self, form):
        self.request.session['site_pk'] = form.site.pk
        return redirect(reverse('webapp:site_detail', args=(form.site.pk,)))


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
            date = form.cleaned_data.get('date')
            site_pks = self.request.POST.getlist('site_pks')
            self._batch_update(date, site_pks)
            messages.success(self.request, Messages.BatchUpdate.success)
        else:
            messages.error(self.request, Messages.BatchUpdate.error)
        return redirect(self.get_success_url())

    def _batch_update(self, date, site_pks):
        if 'set_sites_next_survey_date' in self.request.POST:
            self._batch_update_sites(date, site_pks)
        else:
            self._batch_update_hazards(date, site_pks)

    def _batch_update_sites(self, date, site_pks):
        models.Site.objects.filter(pk__in=site_pks).update(next_survey_date=date)

    def _batch_update_hazards(self, date, site_pks):
        for site_pk in site_pks:
            models.Site.objects.get(pk=site_pk).hazards.update(due_install_test_date=date)

    def get_success_url(self):
        return reverse('webapp:batch_update')