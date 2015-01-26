from django import template
from django.core.exceptions import ObjectDoesNotExist


register = template.Library()


@register.inclusion_tag('hazard_list.html', takes_context=True)
def include_hazards(context, service_type):
    surveys = context['site'].surveys.filter(service_type__service_type=service_type)
    try:
        survey = surveys.latest()
        hazards = survey.hazards.all()
    except ObjectDoesNotExist:
        hazards = []
    if service_type == 'fire':
        context['fire'] = True
    context['hazards'] = hazards
    return context