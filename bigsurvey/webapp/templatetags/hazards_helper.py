from django import template
from main.parameters import BP_TYPE_CHOICES


register = template.Library()


@register.inclusion_tag('hazard/partial/bp_type_checkboxes.html')
def render_bp_type_checkboxes(current_bp_type):
    return {'current_bp_type': current_bp_type, 'bp_types': BP_TYPE_CHOICES}