from django import template

register = template.Library()


@register.simple_tag
def uikit_alert_class(tags):
    if tags == 'error':
        tags = 'danger'
    return tags