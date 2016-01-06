from .base_views import BaseTemplateView, BaseFormView
from django.http import Http404
from django.core.urlresolvers import reverse
from webapp import filters, models, forms, perm_checkers
from django.views.generic import CreateView, UpdateView
from main.parameters import BP_TYPE, Messages, Groups


class SurveyListView(BaseTemplateView):
    template_name = 'survey/survey_list.html'
    permission = "webapp.browse_survey"

    def get_context_data(self, **kwargs):
        context = super(SurveyListView, self).get_context_data(**kwargs)
        surveys = self._get_survey_list()
        context['survey_filter'] = filters.SurveyFilter(self.request.GET, queryset=surveys)
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

    def get_context_data(self, **kwargs):
        context = super(SurveyBaseFormView, self).get_context_data(**kwargs)
        context['hazard_form'] = forms.HazardForm()
        return context

    def get_form(self, form_class):
        form = super(SurveyBaseFormView, self).get_form(form_class)
        form.fields['surveyor'].queryset = self._get_queryset_for_surveyor_field()
        form.fields['hazards'].queryset = self._get_queryset_for_hazards_field(form.instance)
        return form

    def _get_queryset_for_hazards_field(self, survey):
        try:
            site = survey.site
            service_type = survey.service_type
        except AttributeError:
            site = models.Site.objects.get(pk=self.kwargs['pk'])
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
            )
        if self.request.user.has_perm('webapp.access_to_all_surveys'):
            queryset = models.User.objects.filter(groups__name=Groups.surveyor)
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


class SurveyAddView(SurveyBaseFormView, CreateView):
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

    def form_valid(self, form):
        site = self._get_site()
        form.instance.site = site
        form.instance.service_type = self._get_service_type()
        response = super(SurveyAddView, self).form_valid(form)
        self._update_last_survey_date(site)
        self._switch_on_service_type(site, form.instance.service_type.service_type)
        if len(form.cleaned_data['hazards']) == 0:
            form.instance.add_nhp_hazard()
        self._update_is_present(site, form.instance)
        return response

    def _get_site(self):
        site = models.Site.objects.get(pk=self.kwargs['pk'])
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

    def get_form(self, form_class):
        if not perm_checkers.SitePermChecker.has_perm(self.request, self._get_site()):
            raise Http404
        return super(SurveyAddView, self).get_form(form_class)


class SurveyEditView(SurveyBaseFormView, UpdateView):
    permission = 'webapp.add_survey'
    success_message = Messages.Survey.editing_success
    error_message = Messages.Survey.editing_error

    def get_context_data(self, **kwargs):
        context = super(SurveyEditView, self).get_context_data(**kwargs)
        context['site_pk'] = self.object.site.pk
        context['service_type'] = self.object.service_type.service_type.lower()
        return context

    def get_form(self, form_class):
        form = super(SurveyEditView, self).get_form(form_class)
        if not perm_checkers.SurveyPermChecker.has_perm(self.request, form.instance):
            raise Http404
        return form

    def form_valid(self, form):
        site = form.instance.site
        response = super(SurveyEditView, self).form_valid(form)
        self._update_last_survey_date(site)
        self._update_is_present(site, form.instance)
        return response