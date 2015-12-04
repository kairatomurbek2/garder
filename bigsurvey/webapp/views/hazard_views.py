from .base_views import BaseTemplateView, BaseFormView
from django.http import Http404, JsonResponse
from django.core.urlresolvers import reverse
from webapp import filters, models, forms, perm_checkers
from django.views.generic import CreateView, UpdateView
from main.parameters import BP_TYPE, Messages, TESTER_ASSEMBLY_STATUSES
from django.contrib import messages
from webapp.raw_sql_queries import HazardPriorityQuery
from django.db import connection
from django.db.models import Min
from webapp.utils import photo_util
from django.shortcuts import HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import render_to_string


class HazardListView(BaseTemplateView):
    template_name = 'hazard/hazard_list.html'
    permission = "webapp.browse_hazard"

    def get_context_data(self, **kwargs):
        context = super(HazardListView, self).get_context_data(**kwargs)
        hazards = self._get_hazard_list()
        context['hazard_filter'] = filters.HazardFilter(self.request.GET, queryset=hazards)
        return context

    def _get_hazard_list(self):
        user = self.request.user
        queryset = models.Hazard.objects.none()
        if user.has_perm('webapp.access_to_all_hazards'):
            queryset = models.Hazard.objects.all()
        elif user.has_perm('webapp.access_to_pws_hazards'):
            queryset = (models.Hazard.objects.filter(site__pws__in=user.employee.pws.all(), is_present=True) |
                        models.Hazard.objects.filter(tests__tester=user)).distinct()
        sql_query_for_priority = HazardPriorityQuery.get_query(connection.vendor)
        return queryset.extra(select={'priority': sql_query_for_priority}, order_by=('priority',))


class HazardDetailView(BaseTemplateView):
    template_name = 'hazard/hazard.html'
    permission = 'webapp.browse_hazard'

    def get_context_data(self, **kwargs):
        context = super(HazardDetailView, self).get_context_data(**kwargs)
        context['hazard'] = self._get_hazard()
        if not context['hazard'].bp_type_present:
            if not self.request.user.has_perm('webapp.change_all_info_about_hazard') and not self.request.user.employee.has_licence_for_installation:
                messages.error(self.request, Messages.Test.assembly_type_not_set_no_licence)
            else:
                messages.warning(self.request, Messages.Test.assembly_type_not_set % reverse('webapp:hazard_edit', args=(context['hazard'].pk,)))
        context['countlte0'] = self._is_tests_count_lte0(context['hazard'])
        context['BP_TYPE'] = BP_TYPE
        return context

    def _get_hazard(self):
        hazard = models.Hazard.objects.get(pk=self.kwargs['pk'])
        if not perm_checkers.HazardPermChecker.has_perm(self.request, hazard):
            raise Http404
        return hazard

    def _is_tests_count_lte0(self, hazard):
        tests_count = models.Test.objects.filter(bp_device=hazard, tester=self.request.user, paid=True).count()
        return tests_count <= 0


class HazardBaseFormView(BaseFormView):
    template_name = 'hazard/hazard_form.html'
    form_class = forms.HazardForm
    form_class_for_tester = forms.HazardFormForTester
    model = models.Hazard

    def get_success_url(self):
        return reverse('webapp:hazard_detail', args=(self.object.pk,))

    def form_valid(self, form):
        self.object = form.save()
        if self.request.FILES.get('photo'):
            photo_thumb = photo_util.create_thumbnail(self.object.photo)
            self.object.photo_thumb.save(self.object.photo.name, photo_thumb)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.get_success_url())


class HazardAddView(HazardBaseFormView, CreateView):
    permission = 'webapp.add_hazard'
    success_message = Messages.Hazard.adding_success
    error_message = Messages.Hazard.adding_error

    AJAX_OK = 'ok'
    AJAX_ERROR = 'error'

    def get_context_data(self, **kwargs):
        context = super(HazardAddView, self).get_context_data(**kwargs)
        context['site_pk'] = self.kwargs['pk']
        context['service_type'] = self.kwargs['service']
        return context

    def ajax_response(self, status, form):
        json_data = {}
        context = self.get_context_data()
        if status == self.AJAX_OK:
            context['form'] = forms.HazardForm()
            json_data['option'] = {
                'value': self.object.pk,
                'text': str(self.object)
            }
        else:
            context['form'] = form
        json_data['status'] = status
        json_data['form'] = render_to_string('hazard/partial/hazard_form.html', context, RequestContext(self.request))
        return JsonResponse(json_data)

    def get_form(self, form_class):
        site = models.Site.objects.get(pk=self.kwargs['pk'])
        if not perm_checkers.SitePermChecker.has_perm(self.request, site):
            raise Http404
        return super(HazardAddView, self).get_form(form_class)

    def form_valid(self, form):
        form.instance.site = models.Site.objects.get(pk=self.kwargs['pk'])
        form.instance.service_type = models.ServiceType.objects.get(service_type=self.kwargs['service'])
        response = super(HazardAddView, self).form_valid(form)
        self._update_site(form.instance.site, self.kwargs['service'])
        if self.request.is_ajax():
            return self.ajax_response(self.AJAX_OK, form)
        return response

    def _update_site(self, site, service_type):
        if service_type == 'potable':
            site.potable_present = True
        elif service_type == 'fire':
            site.fire_present = True
        elif service_type == 'irrigation':
            site.irrigation_present = True
        site.due_install_test_date = site.hazards.aggregate(
            Min('due_test_date')
        )['due_test_date__min']
        site.save()

    def form_invalid(self, form):
        response = super(HazardAddView, self).form_invalid(form)
        if self.request.is_ajax():
            return self.ajax_response(self.AJAX_ERROR, form)
        return response


class HazardEditView(HazardBaseFormView, UpdateView):
    permission = 'webapp.change_hazard'
    success_message = Messages.Hazard.editing_success
    error_message = Messages.Hazard.editing_error

    def get_form_class(self):
        if self.request.user.has_perm('webapp.change_all_info_about_hazard'):
            return self.form_class
        else:
            return self.form_class_for_tester

    def get_form(self, form_class):
        form = super(HazardEditView, self).get_form(form_class)
        if not perm_checkers.HazardPermChecker.has_perm(self.request, form.instance):
            raise Http404
        if not self.request.user.has_perm('webapp.change_all_info_about_hazard') and not self.request.user.employee.has_licence_for_installation:
            raise Http404
        form.fields['assembly_status'].queryset = self._get_queryset_for_assembly_status_field()
        return form

    def _get_queryset_for_assembly_status_field(self):
        if self.request.user.has_perm('webapp.change_all_info_about_hazard'):
            queryset = models.AssemblyStatus.objects.all()
        else:
            queryset = models.AssemblyStatus.objects.filter(assembly_status__in=TESTER_ASSEMBLY_STATUSES)
        return queryset

    def form_valid(self, form):
        response = super(HazardEditView, self).form_valid(form)
        self._update_site(form.instance.site)
        return response

    def _update_site(self, site):
        site.due_install_test_date = site.hazards.aggregate(
            Min('due_test_date')
        )['due_test_date__min']
        site.save()
