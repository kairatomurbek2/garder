from django import template
import webapp.models as models


register = template.Library()


@register.inclusion_tag('survey_list.html', takes_context=True)
def include_surveys(context, service_type):
    surveys = context['site'].surveys.filter(service_type__service_type=service_type)
    context['surveys'] = surveys
    context['countlte0'] = True
    if surveys.count() > 0:
        context['countlte0'] = False
    if service_type == 'fire':
        context['fire'] = True
    context['service_type_pk'] = models.ServiceType.objects.get(service_type=service_type).pk
    return context