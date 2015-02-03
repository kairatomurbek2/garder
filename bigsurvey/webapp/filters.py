import django_filters
import models
from main.parameters import DATE_FILTER_CHOICES
from datetime import datetime, timedelta


def site_status_choices():
    choices = [('', 'All')]
    for status in models.SiteStatus.objects.all():
        choices.append((status.pk, status.site_status))
    return choices


def site_use_choices():
    choices = [('', 'All')]
    for site_use in models.SiteUse.objects.all().order_by('site_use'):
        choices.append((site_use.pk, site_use.site_use))
    return choices


def site_type_choices():
    choices = [('', 'All')]
    for site_type in models.SiteType.objects.all().order_by('site_type'):
        choices.append((site_type.pk, site_type.site_type))
    return choices


def customer_filter(sites, value):
    if value:
        customers = models.Customer.objects.filter(number__icontains=value) | models.Customer.objects.filter(name__icontains=value)
        return sites.filter(customer__in=customers)
    return sites


def next_date_filter(sites, value):
    current_date = datetime.now()

    dates = {
        'week': current_date + timedelta(weeks=1),
        'month': current_date + timedelta(days=30),
        'year': current_date + timedelta(days=365),
    }

    if value in dates:
        return sites.filter(next_survey_date__range=[current_date, dates[value]])
    return sites


class SiteFilter(django_filters.FilterSet):
    customer = django_filters.CharFilter(label='', action=customer_filter)
    city = django_filters.CharFilter(lookup_type='icontains', label='')
    address = django_filters.CharFilter(lookup_type='icontains', label='', name='address1')
    site_type = django_filters.ChoiceFilter(choices=site_type_choices(), label='')
    site_use = django_filters.ChoiceFilter(choices=site_use_choices(), label='')
    status = django_filters.ChoiceFilter(choices=site_status_choices(), label='')
    next_survey_date = django_filters.ChoiceFilter(choices=DATE_FILTER_CHOICES, action=next_date_filter, label='')

    class Meta:
        models = models.Site
        fields = [
            'customer',
            'city',
            'address1',
            'site_use',
            'site_type',
            'status',
            'next_survey_date'
        ]