from django.contrib import messages
from django.core.urlresolvers import reverse
from django.forms import formset_factory, BooleanField, HiddenInput
from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils.functional import curry
from django.views.generic import UpdateView
from main.parameters import BP_TYPE, Messages, Groups, ASSEMBLY_STATUSES_WITH_BP
from webapp import filters, models, forms, perm_checkers
from .base_views import BaseTemplateView, BaseFormView


class SurveyListView(BaseTemplateView):
    template_name = 'survey/survey_list.html'
    permission = "webapp.browse_survey"

    def get_context_data(self, **kwargs):
        context = super(SurveyListView, self).get_context_data(**kwargs)
        surveys = self._get_survey_list()
        context['survey_filter'] = filters.SurveyFilter(self.request.GET, queryset=surveys, user=self.request.user)
        return context

    def _get_survey_list(self):
        user = self.request.user
        if user.has_perm("webapp.access_to_all_surveys"):
            return models.Survey.objects.all()
        if user.has_perm("webapp.access_to_pws_surveys"):
            return models.Survey.objects.filter(site__pws__in=user.employee.pws.all())
        if user.has_perm("webapp.access_to_own_surveys"):
            return models.Survey.objects.filter(surveyor=user, site__pws__in=user.employee.pws.all())


class SurveyDetailView(BaseTemplateView):
    template_name = 'survey/survey.html'
    permission = 'webapp.browse_survey'

    def get_context_data(self, **kwargs):
        survey = models.Survey.objects.get(pk=self.kwargs['pk'])
        if not perm_checkers.SurveyPermChecker.has_perm(self.request, survey):
            raise Http404
        context = super(SurveyDetailView, self).get_context_data(**kwargs)
        context['survey'] = survey
        context['hazards'] = survey.hazards.all()
        context['service'] = survey.service_type.service_type
        context['BP_TYPE'] = BP_TYPE
        return context


class SurveyBaseFormView(BaseFormView):
    template_name = 'survey/survey_form.html'
    form_class = forms.SurveyForm
    model = models.Survey
    hazard_form_class = forms.HazardFormForSurvey
    bp_form_class = forms.BPForm
    hazard_error_message = Messages.Hazard.adding_error
    survey_added_message = Messages.Survey.adding_success

    def get_hazard_formset(self):
        HazardFormset = formset_factory(self.hazard_form_class)
        HazardFormset.form = staticmethod(
            curry(self.hazard_form_class, letter_types_qs=self._get_queryset_for_letter_type_field()))
        return HazardFormset

    def get_context_data(self, **kwargs):
        context = super(SurveyBaseFormView, self).get_context_data(**kwargs)
        HazardFormset = self.get_hazard_formset()
        BPFormset = formset_factory(self.bp_form_class)
        context['hazard_formset'] = HazardFormset(prefix='hazard')
        context['bp_formset'] = BPFormset(prefix='bp')
        context['allow_adding_hazards'] = True
        return context

    def get_form(self, form_class):
        form = super(SurveyBaseFormView, self).get_form(form_class)
        form.prefix = 'survey'
        form.fields['surveyor'].queryset = self._get_queryset_for_surveyor_field()
        form.fields['hazards'].queryset = self._get_queryset_for_hazards_field(form.instance)
        return form

    def get_bp_form(self):
        kwargs = {
            'initial': {},
            'prefix': 'bp',
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return self.bp_form_class(**kwargs)

    def get_hazard_form(self):
        kwargs = {
            'initial': {},
            'prefix': 'hz',
            'letter_types_qs': self._get_queryset_for_letter_type_field()
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return self.hazard_form_class(**kwargs)

    def _get_queryset_for_hazards_field(self, survey):
        try:
            site = survey.site
            service_type = survey.service_type
        except AttributeError:
            site = models.Site.active_only.get(pk=self.kwargs['pk'])
            service_type = models.ServiceType.objects.get(service_type=self.kwargs['service'])
        return site.hazards.filter(service_type=service_type)

    def _get_queryset_for_surveyor_field(self):
        queryset = models.User.objects.none()
        if self.request.user.has_perm('webapp.access_to_own_surveys'):
            queryset = models.User.objects.filter(pk=self.request.user.pk)
        if self.request.user.has_perm('webapp.access_to_pws_surveys'):
            queryset = models.User.objects.filter(
                groups__name=Groups.surveyor,
                employee__pws__in=self.request.user.employee.pws.all()
            ).distinct()
        if self.request.user.has_perm('webapp.access_to_all_surveys'):
            queryset = models.User.objects.filter(groups__name=Groups.surveyor)
        return queryset

    def _get_queryset_for_letter_type_field(self):
        site = models.Site.active_only.get(pk=self.kwargs['pk'])
        queryset = models.LetterType.objects.filter(pws=site.pws)
        return queryset

    def _update_last_survey_date(self, site):
        survey = site.surveys.latest('survey_date')
        site.last_survey_date = survey.survey_date
        site.save()

    def _update_is_present(self, site, survey):
        survey.hazards.update(is_present=True)
        site.hazards.filter(service_type=survey.service_type).exclude(pk__in=(hazard.pk for hazard in survey.hazards.all())).update(is_present=False)

    def get_success_url(self):
        return reverse('webapp:survey_detail', args=(self.object.pk,))


class SurveyEditView(SurveyBaseFormView, UpdateView):
    permission = 'webapp.add_survey'
    success_message = Messages.Survey.editing_success
    error_message = Messages.Survey.editing_error

    def get_context_data(self, **kwargs):
        context = super(SurveyEditView, self).get_context_data(**kwargs)
        context['site_pk'] = self.object.site.pk
        context['service_type'] = self.object.service_type.service_type.lower()
        survey = models.Survey.objects.get(pk=self.kwargs['pk'])
        if survey.site.surveys.all().order_by('-pk').first() != survey:
            context['allow_adding_hazards'] = False
        return context

    def get_form(self, form_class):
        form = super(SurveyEditView, self).get_form(form_class)
        if not perm_checkers.SurveyPermChecker.has_perm(self.request, form.instance):
            raise Http404
        survey = form.instance
        if survey.site.surveys.all().order_by('-pk').first() != survey:
            del form.fields['hazards']
        return form

    def form_valid(self, form):
        survey = form.instance
        site = survey.site
        hazards = survey.hazards.all()
        response = super(SurveyEditView, self).form_valid(form)
        self._update_last_survey_date(site)
        if survey.site.surveys.all().order_by('-pk').first() == survey:
            self._update_is_present(site, survey)
        else:
            self.object.hazards = hazards
            self.object.save()
        return response


class SurveyAddView(SurveyBaseFormView):
    permission = 'webapp.add_survey'
    success_message = Messages.Survey.adding_success
    error_message = Messages.Survey.adding_error

    def get_context_data(self, **kwargs):
        context = super(SurveyAddView, self).get_context_data(**kwargs)
        context['site_pk'] = self.kwargs['pk']
        context['service_type'] = self.kwargs['service']
        context['fire'] = self._is_fire_service()
        return context

    def _is_fire_service(self):
        if self.kwargs['service'] == 'fire':
            return True
        return False


    def post(self, request, *args, **kwargs):
        survey_form = self.get_survey_form(self.form_class)
        HazardFormset = self.get_hazard_formset()
        hazard_formset = HazardFormset(request.POST, request.FILES, prefix='hazard')
        BPFormset = formset_factory(self.bp_form_class)
        bp_formset = BPFormset(request.POST, request.FILES, prefix='bp')
        if hazard_formset.is_valid() and survey_form.is_valid():
            site = self.get_site()
            if hazard_formset.has_changed():
                new_hazards = self._create_hazards_and_update_related_objects(site, hazard_formset, bp_formset)
            else:
                new_hazards = []
            self._create_survey_and_update_related_objects(site, survey_form, new_hazards)
            messages.success(request, self.survey_added_message)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(survey_form, HazardFormset, BPFormset)

    def form_invalid(self, survey_form, HazardFormset, BPFormset):
        if self.hazard_error_message:
            messages.error(self.request, self.hazard_error_message)
        return render_to_response(self.template_name, self.get_context_data(
            form=survey_form,
            hazard_formset=HazardFormset(prefix='hazard'),
            bp_formset=BPFormset(prefix='bp')))

    @staticmethod
    def device_present_from_formset(hazard_formset):
        for hazard_form in hazard_formset:
            if hazard_form.cleaned_data['assembly_status'] in ASSEMBLY_STATUSES_WITH_BP:
                return True
            return False

    @staticmethod
    def device_present_from_form(hazard_form):
        if hazard_form.cleaned_data['assembly_status'] in ASSEMBLY_STATUSES_WITH_BP:
            return True
        return False

    def _create_hazards_and_update_related_objects(self, site, hazard_formset, bp_formset):
        service_type = self._get_service_type()
        new_hazards = []
        for i in xrange(len(hazard_formset)):
            hazard_form = hazard_formset[i]
            hazard_form.instance.site = site
            hazard_form.instance.service_type = service_type
            if self.device_present_from_form(hazard_form):
                bp_device = bp_formset[i].save()
            else:
                bp_device = None
            hazard_obj = hazard_form.save()
            hazard_obj.bp_device = bp_device
            hazard_obj.save()
            hazard_obj.update_due_install_test_date(service_type)
            new_hazards.append(hazard_obj)
        return new_hazards

    def _create_survey_and_update_related_objects(self, site, survey_form, new_hazards):
        survey_form.instance.site = site
        survey_form.instance.service_type = self._get_service_type()
        self.object = survey_form.save()
        self._update_last_survey_date(site)
        self._switch_on_service_type(site, survey_form.instance.service_type.service_type)
        if len(survey_form.cleaned_data['hazards']) == 0 and len(new_hazards) == 0:
            survey_form.instance.add_nhp_hazard()
        if len(new_hazards) > 0:
            for new_hazard in new_hazards:
                survey_form.instance.hazards.add(new_hazard)
        self._update_is_present(site, survey_form.instance)

    def get_site(self):
        site = models.Site.active_only.get(pk=self.kwargs['pk'])
        if not perm_checkers.SitePermChecker.has_perm(self.request, site):
            raise Http404
        return site

    def _get_service_type(self):
        return models.ServiceType.objects.filter(service_type__icontains=self.kwargs['service'])[0]

    def _switch_on_service_type(self, site, service_type):
        if service_type == 'potable':
            site.potable_present = True
        elif service_type == 'fire':
            site.fire_present = True
        elif service_type == 'irrigation':
            site.irrigation_present = True
        site.save()

    def get_survey_form(self, form_class):
        if not perm_checkers.SitePermChecker.has_perm(self.request, self.get_site()):
            raise Http404
        return super(SurveyAddView, self).get_form(form_class)
