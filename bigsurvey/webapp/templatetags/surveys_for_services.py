from django import template


register = template.Library()


@register.inclusion_tag('survey/survey_include_list.html', takes_context=True)
def include_surveys(context, service_type):
    context['surveys'] = context['surv_%s' % service_type[0]]
    context['service'] = service_type
    return context