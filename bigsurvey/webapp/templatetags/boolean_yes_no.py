from django import template
from main.parameters import YESNO_CHOICES


register = template.Library()


@register.filter(name='yn')
def bool_yn(bool_value):
    for choice in YESNO_CHOICES:
        if choice[0] == bool_value:
            return choice[1]