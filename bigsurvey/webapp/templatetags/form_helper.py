from django import template


register = template.Library()


@register.filter()
def xrange_filter(start_num, end_num=None, step=None):
    if end_num is None:
        return xrange(0, int(start_num))
    if step is None:
        return xrange(int(start_num), int(end_num))
    return xrange(int(start_num), int(end_num), int(step))


@register.assignment_tag()
def get_formset_index(row_index, col_index):
    return int(row_index) * 2 + int(col_index)


@register.assignment_tag()
def get_form_from_formset(formset, index):
    try:
        return formset.forms[int(index)]
    except IndexError:
        pass