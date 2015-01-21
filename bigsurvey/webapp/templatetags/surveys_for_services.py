from django import template


register = template.Library()


@register.inclusion_tag('survey_list.html')
def include_surveys(site, service_type):
    service = site.services.filter(service_type__service_type=service_type)[0]
    return {'surveys': service.surveys.all()}