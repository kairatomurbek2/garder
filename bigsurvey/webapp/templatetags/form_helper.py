from django import template


register = template.Library()


@register.inclusion_tag('partial/radiobuttons.html')
def render_radiobuttons(radiobuttons):
    return {'radiobuttons': radiobuttons}


@register.inclusion_tag('partial/checkboxes.html')
def render_checkboxes(checkboxes):
    return {'checkboxes': checkboxes}