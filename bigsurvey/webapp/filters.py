import django_filters
import models
from main.parameters import DATE_FILTER_CHOICES
from datetime import datetime, timedelta
from django.utils.translation import ugettext_lazy as _


def site_status_choices():
    choices = [('', _('All'))]
    for status in models.SiteStatus.objects.all():
        choices.append((status.pk, status.site_status))
    return choices


def site_use_choices():
    choices = [('', _('All'))]
    for site_use in models.SiteUse.objects.all().order_by('site_use'):
        choices.append((site_use.pk, site_use.site_use))
    return choices


def site_type_choices():
    choices = [('', _('All'))]
    for site_type in models.SiteType.objects.all().order_by('site_type'):
        choices.append((site_type.pk, site_type.site_type))
    return choices


def pws_choices():
    choices = [('', _('All'))]
    for pws in models.PWS.objects.all().order_by('name'):
        choices.append((pws.pk, pws.name))
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
    customer = django_filters.CharFilter(label=_('Customer Name or Account'), action=customer_filter)
    city = django_filters.CharFilter(lookup_type='icontains', label=_('Site City'))
    address = django_filters.CharFilter(lookup_type='icontains', label=_('Site Address'), name='address1')
    pws = django_filters.ChoiceFilter(choices=pws_choices(), label=_('PWS'))
    site_type = django_filters.ChoiceFilter(choices=site_type_choices(), label=_('Site Type'))
    site_use = django_filters.ChoiceFilter(choices=site_use_choices(), label=_('Site Use'))
    status = django_filters.ChoiceFilter(choices=site_status_choices(), label=_('Site Status'))
    next_survey_date = django_filters.ChoiceFilter(choices=DATE_FILTER_CHOICES, action=next_date_filter,
                                                   label=_('Next Survey Date'))

    class Meta:
        models = models.Site
        fields = [
            'customer',
            'city',
            'pws',
            'address1',
            'site_use',
            'site_type',
            'status',
            'next_survey_date',
        ]