from django import template
from django.template import Variable, VariableDoesNotExist


register = template.Library()


@register.assignment_tag()
def resolve(target, lookup):
    try:
        return Variable(lookup).resolve(target)
    except VariableDoesNotExist:
        return None