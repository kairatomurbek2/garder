from django import template

register = template.Library()

@register.inclusion_tag('partial/replaced_details.html')
def render_replaced_details(details):
    return {'details': details}