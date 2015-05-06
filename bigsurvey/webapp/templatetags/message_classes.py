from django import template

register = template.Library()


@register.simple_tag
def uikit_class(tags):
    return 'danger' if tags == 'error' else tags