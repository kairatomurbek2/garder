from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import connection
from django.http import Http404
from django.shortcuts import HttpResponseRedirect
from django.views.generic import UpdateView
from main.parameters import BP_TYPE, Messages, ASSEMBLY_STATUSES_WITH_BP, AssemblyStatus
from webapp import filters, models, forms, perm_checkers
from webapp.raw_sql_queries import HazardPriorityQuery
from webapp.utils import photo_util
from .base_views import BaseTemplateView, BaseFormView


class HazardListView(BaseTemplateView):
    template_name = 'hazard/hazard_list.html'
    permission = "webapp.browse_hazard"

    def get_context_data(self, **kwargs):
        context = super(HazardListView, self).get_context_data(**kwargs)
        hazards = self._get_hazard_list()
        context['hazard_filter'] = filters.HazardFilter(self.request.GET, queryset=hazards, user=self.request.user)
        return context

    def _get_hazard_list(self):
        user = self.request.user
        queryset = models.Hazard.objects.none()
        if user.has_perm('webapp.access_to_all_hazards'):
            queryset = models.Hazard.objects.all()
        elif user.has_perm('webapp.access_to_pws_hazards'):
            queryset = models.Hazard.objects.filter(site__pws__in=user.employee.pws.all(), is_present=True)
        else:
            raise Http404
        sql_query_for_priority = HazardPriorityQuery.get_query(connection.vendor)
        return queryset.extra(select={'priority': sql_query_for_priority}, order_by=('priority',))


class HazardDetailView(BaseTemplateView):
    template_name = 'hazard/hazard.html'
    permission = 'webapp.browse_hazard'

    def get_context_data(self, **kwargs):
        context = super(HazardDetailView, self).get_context_data(**kwargs)
        hazard = self._get_hazard()
        context['hazard'] = hazard
        context['countlte0'] = self._is_tests_count_lte0(context['hazard'])
        context['show_install_button'] = self.show_install_button()
        context['BP_TYPE'] = BP_TYPE
        context['show_back_button'] = self.show_back_button(hazard)
        self._set_warn_messages(hazard)
        return context

    def _set_warn_messages(self, hazard):
        if self._device_present(hazard):
            if not hazard.bp_device:
                messages.warning(self.request, Messages.Hazard.device_absence_warning %
                                 hazard.get_assembly_status_display())
        else:
            if hazard.bp_device:
                messages.warning(self.request, Messages.Hazard.device_presence_warning %
                                 hazard.get_assembly_status_display())
        if not hazard.is_present:
            messages.warning(self.request, Messages.Hazard.hazard_inactive)

    def _get_hazard(self):
        hazard = models.Hazard.objects.get(pk=self.kwargs['pk'])
        if not perm_checkers.HazardPermChecker.has_perm(self.request, hazard):
            raise Http404
        return hazard

    def _device_present(self, hazard):
        if hazard.assembly_status in ASSEMBLY_STATUSES_WITH_BP:
            return True
        return False

    def show_back_button(self, hazard):
        user = self.request.user
        if user.has_perm('webapp.access_to_all_sites') or user.has_perm('webapp.access_to_pws_sites'):
            return True
        if user.has_perm('webapp.access_to_site_by_customer_account'):
            session_site_pks = self.request.session.get('sites_pks')
            if session_site_pks:
                if hazard.site.pk in session_site_pks:
                    return True
        return False

    def show_install_button(self):
        user = self.request.user
        return not user.has_perm('webapp.change_hazard') \
               and user.has_perm('webapp.change_bpdevice') and user.employee.has_licence_for_installation

    def _is_tests_count_lte0(self, hazard):
        tests_count = models.Test.objects.filter(bp_device=hazard, tester=self.request.user, paid=True).count()
        return tests_count <= 0


class HazardBaseFormView(BaseFormView):
    template_name = 'hazard/hazard_form.html'
    form_class = forms.HazardForm
    model = models.Hazard

    def get_form_kwargs(self):
        kwargs = super(HazardBaseFormView, self).get_form_kwargs()
        form_data = {'letter_types_qs': self._get_queryset_for_letter_type_field()}
        kwargs['letter_types_qs'] = form_data
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(HazardBaseFormView, self).get_context_data(**kwargs)
        context['hazard_form'] = forms.HazardForm()
        return context

    def get_form(self, form_class):
        form = super(HazardBaseFormView, self).get_form(form_class)
        form.fields['letter_type'].queryset = self._get_queryset_for_letter_type_field()
        return form

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

    def _get_queryset_for_letter_type_field(self):
        site = models.Site.objects.get(pk=self.kwargs['pk'])
        queryset = models.LetterType.objects.filter(pws=site.pws)
        return queryset


class HazardEditView(HazardBaseFormView, UpdateView):
    permission = 'webapp.change_hazard'
    success_message = Messages.Hazard.editing_success
    error_message = Messages.Hazard.editing_error

    def get_context_data(self, **kwargs):
        context = super(HazardEditView, self).get_context_data(**kwargs)
        context['hazard_pk'] = self.kwargs['pk']
        return context

    def get_form(self, form_class):
        form = super(HazardEditView, self).get_form(form_class)
        if not perm_checkers.HazardPermChecker.has_perm(self.request, form.instance):
            raise Http404
        return form

    def device_present(self, form):
        return not form.cleaned_data['assembly_status'] == AssemblyStatus.DUE_INSTALL

    def form_valid(self, form):
        response = super(HazardEditView, self).form_valid(form)
        if not self.device_present(form):
            form.instance.bp_device = None
            form.instance.save()
        form.instance.update_site()
        return response
