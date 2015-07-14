from django import template
from main.parameters import YESNO_CHOICES, CLEANED_REPLACED_CHOICES, VALVE_LEAKED_CHOICES, VALVE_OPENED_CHOICES, TEST_RESULT_CHOICES


register = template.Library()


@register.filter()
def yn(bool_value):
    for choice in YESNO_CHOICES:
        if choice[0] == bool_value:
            return choice[1]


@register.filter()
def cleaned_replaced(value):
    for choice in CLEANED_REPLACED_CHOICES:
        if choice[0] == value:
            return choice[1]


@register.filter()
def valve_leaked(bool_value):
    for choice in VALVE_LEAKED_CHOICES:
        if choice[0] == bool_value:
            return choice[1]


@register.filter()
def valve_opened(bool_value):
    for choice in VALVE_OPENED_CHOICES:
        if choice[0] == bool_value:
            return choice[1]


@register.filter()
def test_result(bool_value):
    for choice in TEST_RESULT_CHOICES:
        if choice[0] == bool_value:
            return choice[1]