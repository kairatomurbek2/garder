from django import template

register = template.Library()


@register.inclusion_tag('hazard/hazard_list.html', takes_context=True)
def include_hazards(context, service_type):
    context['hazards'] = context['haz_%s' % service_type[0]]
    context['service'] = service_type
    return context