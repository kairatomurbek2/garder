from django import template
from django.core.exceptions import ObjectDoesNotExist


register = template.Library()


@register.inclusion_tag('hazard_list.html', takes_context=True)
def include_hazards(context, service_type):
    service = context['site'].services.filter(service_type__service_type=service_type)[0]
    hazards = []
    try:
        survey = service.surveys.latest()
        hazards = survey.hazards.all()
    except ObjectDoesNotExist:
        pass
    if service_type == 'fire':
        context['fire'] = True
    context['hazards'] = hazards
    return context