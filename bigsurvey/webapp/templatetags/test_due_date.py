from django import template
from django.db.models import Min


register = template.Library()


@register.simple_tag
def get_due_test_date(site):
    date = site.hazards.all().aggregate(Min('due_install_test_date'))['due_install_test_date__min']
    if date:
        return date.strftime("%b. %d, %Y")
    return None
