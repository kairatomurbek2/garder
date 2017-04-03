from django import template
from django.template import Variable, VariableDoesNotExist


register = template.Library()


@register.assignment_tag()
def resolve(target, lookup):
    try:
        return Variable(lookup).resolve(target)
    except VariableDoesNotExist:
        return None


@register.filter()
def verbose_name(object):
    return object._meta.verbose_name


@register.filter(name="has_access")
def has_access(user, access):
    return user.has_perm("webapp.%s" % access)


@register.filter(name="has_group")
def has_access(user, group_name):
    return group_name in [group.name for group in user.groups.all()]


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter(name='string_indent')
def string_indent(value, max_length):
    if len(value) > max_length:
        return "%s\n%s" % (value[:max_length], value[max_length:])
    else:
        return value