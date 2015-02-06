from django import template
from main.parameters import VALVE_LEAKED_CHOICES


register = template.Library()


@register.filter(name='valve_leaked')
def bool_yn(bool_value):
    for choice in VALVE_LEAKED_CHOICES:
        if choice[0] == bool_value:
            return choice[1]