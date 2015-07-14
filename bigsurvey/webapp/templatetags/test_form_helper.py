from django import template

from main.parameters import BP_TYPE
from webapp.models import Detail


register = template.Library()


@register.inclusion_tag('test/partial/test_form_bp_type_checkboxes.html')
def render_bp_type_checkboxes(current_bp_type):
    return {'current_bp_type': current_bp_type, 'bp_types': BP_TYPE.REQUIRE_TEST_TYPES}


@register.inclusion_tag('partial/radiobuttons.html')
def render_radiobuttons(radiobuttons):
    return {'radiobuttons': radiobuttons}


@register.inclusion_tag('partial/checkboxes.html')
def render_checkboxes(checkboxes):
    return {'checkboxes': checkboxes}


@register.filter()
def detail_pk_by_name(name):
    try:
        return Detail.objects.get(detail__iexact=name).pk
    except Detail.DoesNotExist:
        return None


@register.inclusion_tag('test/partial/replaced_details.html')
def render_replaced_details(details):
    return {'details': details}


@register.simple_tag()
def is_detail_checked(details, name):
    try:
        if details.filter(detail__iexact=name).exists():
            return 'checked'
        raise Exception
    except Exception:
        return ''
