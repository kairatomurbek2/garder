from django import template


register = template.Library()


@register.inclusion_tag('survey/survey_list.html', takes_context=True)
def include_surveys(context, service_type):
    surveys = context['site'].surveys.filter(service_type__service_type=service_type)
    context['surveys'] = surveys
    context['countlte0'] = True
    if surveys.count() > 0:
        context['countlte0'] = False
    context['service'] = service_type
    return context