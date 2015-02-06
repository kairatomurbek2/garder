from django import template
from main.parameters import VALVE_OPENED_CHOICES


register = template.Library()


@register.filter(name='valve_opened')
def bool_yn(bool_value):
    for choice in VALVE_OPENED_CHOICES:
        if choice[0] == bool_value:
            return choice[1]