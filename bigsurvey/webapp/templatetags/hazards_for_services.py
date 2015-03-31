from django import template
from django.core.exceptions import ObjectDoesNotExist
from webapp.models import Survey


register = template.Library()


@register.inclusion_tag('hazard/hazard_list.html', takes_context=True)
def include_hazards(context, service_type, survey_pk=0):
    if survey_pk > 0:
        survey = Survey.objects.get(pk=survey_pk)
        hazards = survey.hazards.all()
    else:
        surveys = context['site'].surveys.filter(service_type__service_type=service_type)
        try:
            survey = surveys.latest()
            hazards = survey.hazards.all()
        except ObjectDoesNotExist:
            hazards = []
    context['hazards'] = hazards
    return context