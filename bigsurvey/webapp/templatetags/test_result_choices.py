from django import template
from main.parameters import TEST_RESULT_CHOICES


register = template.Library()


@register.filter(name='test_result')
def bool_yn(bool_value):
    for choice in TEST_RESULT_CHOICES:
        if choice[0] == bool_value:
            return choice[1]