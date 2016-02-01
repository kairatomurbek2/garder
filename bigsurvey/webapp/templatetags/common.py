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
