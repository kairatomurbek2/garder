from django import template
from webapp.models import Detail


register = template.Library()


@register.filter()
def xrange_filter(start_num, end_num=None, step=None):
    if end_num is None:
        return xrange(0, int(start_num))
    if step is None:
        return xrange(int(start_num), int(end_num))
    return xrange(int(start_num), int(end_num), int(step))


@register.inclusion_tag('partial/radiobuttons.html')
def render_radiobuttons(radiobuttons):
    return {'radiobuttons': radiobuttons}


@register.filter()
def detail_pk_by_name(name):
    try:
        return Detail.objects.get(detail__iexact=name).pk
    except Detail.DoesNotExist:
        return None


@register.inclusion_tag('partial/checkboxes.html')
def render_checkboxes(checkboxes):
    return {'checkboxes': checkboxes}


@register.simple_tag()
def is_detail_checked(details, name):
    try:
        if details.filter(detail__iexact=name).exists():
            return 'checked'
        raise Exception
    except Exception:
        return ''


@register.assignment_tag()
def get_formset_index(row_index, col_index):
    return int(row_index) * 2 + int(col_index)


@register.assignment_tag()
def get_form(formset, index):
    try:
        return formset.forms[int(index)]
    except IndexError:
        pass