from django import template


register = template.Library()


@register.filter()
def file_name(object):
    return object.split('/')[-1]


