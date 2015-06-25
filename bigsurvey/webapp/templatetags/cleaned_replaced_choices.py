from django import template
from main.parameters import CLEANED_REPLACED_CHOICES


register = template.Library()

@register.filter()
def cleaned_replaced(value):
    for choice in CLEANED_REPLACED_CHOICES:
        if choice[0] == value:
            return choice[1]