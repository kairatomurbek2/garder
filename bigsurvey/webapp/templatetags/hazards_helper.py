from django import template
from webapp.models import BPType


register = template.Library()


@register.inclusion_tag('hazard/partial/bp_type_checkboxes.html')
def render_bp_type_checkboxes(current_bp_type):
    return {'current_bp_type': current_bp_type, 'bp_types': BPType.objects.all()}