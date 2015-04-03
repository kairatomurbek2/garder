import django_filters
import models
from main.parameters import NEXT_DATE_FILTER_CHOICES, PAST_DATE_FILTER_CHOICES, Groups
from datetime import datetime, timedelta
from django.utils.translation import ugettext_lazy as _


class FilterChoices(object):
    @staticmethod
    def site_status():
        choices = [('', _('All'))]
        for status in models.SiteStatus.objects.all():
            choices.append((status.pk, status.site_status))
        return choices

    @staticmethod
    def site_use():
        choices = [('', _('All'))]
        for site_use in models.SiteUse.objects.all().order_by('site_use'):
            choices.append((site_use.pk, site_use.site_use))
        return choices

    @staticmethod
    def site_type():
        choices = [('', _('All'))]
        for site_type in models.SiteType.objects.all().order_by('site_type'):
            choices.append((site_type.pk, site_type.site_type))
        return choices

    @staticmethod
    def pws():
        choices = [('', _('All'))]
        for pws in models.PWS.objects.all().order_by('name'):
            choices.append((pws.pk, pws.number))
        return choices

    @staticmethod
    def customer_code():
        choices = [('', _('All'))]
        for customer_code in models.CustomerCode.objects.all().order_by('customer_code'):
            choices.append((customer_code.pk, customer_code.customer_code))
        return choices

    @staticmethod
    def service_type():
        choices = [('', _('All'))]
        for service_type in models.ServiceType.objects.all().order_by('service_type'):
            choices.append((service_type.pk, service_type.service_type))
        return choices

    @staticmethod
    def surveyor():
        choices = [('', _('All'))]
        surveyors = models.User.objects.filter(groups__name=Groups.surveyor).order_by('last_name', 'first_name')
        for user in surveyors:
            choices.append((user.pk, user.username))
        return choices

    @staticmethod
    def survey_type():
        choices = [('', _('All'))]
        for survey_type in models.SurveyType.objects.all():
            choices.append((survey_type.pk, survey_type.survey_type))
        return choices


class FilterActions(object):
    class Site(object):
        @staticmethod
        def customer_name(sites, value):
            if value:
                return sites.filter(customer__name__icontains=value)
            return sites

        @staticmethod
        def customer_account(sites, value):
            if value:
                return sites.filter(customer__number__icontains=value)
            return sites

        @staticmethod
        def next_date(sites, value):
            current_date = datetime.now()
            dates = {
                'week': current_date + timedelta(weeks=1),
                'month': current_date + timedelta(days=30),
                'year': current_date + timedelta(days=365),
            }
            if value in dates:
                return sites.filter(next_survey_date__range=[current_date, dates[value]])
            return sites

        @staticmethod
        def last_date(sites, value):
            current_date = datetime.now().date()
            dates = {
                'week': current_date - timedelta(weeks=1),
                'month': current_date - timedelta(days=30),
                '2months': current_date - timedelta(days=30 * 2),
                '3months': current_date - timedelta(days=30 * 3),
                '6months': current_date - timedelta(days=30 * 6),
                'year': current_date - timedelta(days=365),
            }
            if value == 'never':
                return sites.filter(last_survey_date=None)
            if value in dates:
                return sites.filter(last_survey_date__lt=dates[value])
            return sites

    class Survey(object):
        @staticmethod
        def pws(surveys, value):
            if value:
                return surveys.filter(site__pws__id=value)
            return surveys

        @staticmethod
        def site_city(surveys, value):
            if value:
                return surveys.filter(site__city__icontains=value)
            return surveys

        @staticmethod
        def customer_account(surveys, value):
            if value:
                return surveys.filter(site__customer__number__icontains=value)
            return surveys

        @staticmethod
        def surveyor(surveys, value):
            if value:
                return surveys.filter(surveyor__id=value)
            return surveys

        @staticmethod
        def site_address(surveys, value):
            if value:
                return surveys.filter(site__address1__icontains=value)
            return surveys


class SiteFilter(django_filters.FilterSet):
    pws = django_filters.ChoiceFilter(choices=FilterChoices.pws(), label=_('PWS'))
    customer_name = django_filters.CharFilter(label=_('Customer Name'),
                                              action=FilterActions.Site.customer_name)
    customer_account = django_filters.CharFilter(label=_('Customer Account'),
                                                 action=FilterActions.Site.customer_account)
    city = django_filters.CharFilter(lookup_type='icontains', label=_('Site City'))
    address = django_filters.CharFilter(lookup_type='icontains', label=_('Site Address'), name='address1')
    site_type = django_filters.ChoiceFilter(choices=FilterChoices.site_type(), label=_('Site Type'))
    site_use = django_filters.ChoiceFilter(choices=FilterChoices.site_use(), label=_('Site Use'))
    status = django_filters.ChoiceFilter(choices=FilterChoices.site_status(), label=_('Site Status'))
    next_survey_date = django_filters.ChoiceFilter(choices=NEXT_DATE_FILTER_CHOICES,
                                                   action=FilterActions.Site.next_date,
                                                   label=_('Next Survey Date'))
    last_survey_date = django_filters.ChoiceFilter(choices=PAST_DATE_FILTER_CHOICES,
                                                   action=FilterActions.Site.last_date,
                                                   label=_('Last Survey older than'))

    class Meta:
        models = models.Site
        fields = [
            'pws',
            'customer',
            'city',
            'address1',
            'site_use',
            'site_type',
            'status',
            'next_survey_date',
            'last_survey_date',
        ]


class CustomerFilter(django_filters.FilterSet):
    number = django_filters.CharFilter(label=_('Account Number'), lookup_type='icontains')
    name = django_filters.CharFilter(label=_('Customer Name'), lookup_type='icontains')
    code = django_filters.ChoiceFilter(label=_('Customer Code'), choices=FilterChoices.customer_code())
    city = django_filters.CharFilter(label=_('City'), lookup_type='icontains')
    address = django_filters.CharFilter(label=_('Address'), lookup_type='icontains', name='address1')
    zip = django_filters.CharFilter(label=_('ZIP'), lookup_type='icontains')

    class Meta:
        models = models.Customer
        fields = [
            'number'
            'name'
            'city'
            'address1'
            'zip'
        ]


class SurveyFilter(django_filters.FilterSet):
    pws = django_filters.ChoiceFilter(choices=FilterChoices.pws(), label=_('PWS'), action=FilterActions.Survey.pws)
    customer = django_filters.CharFilter(label=_('Customer Account'), action=FilterActions.Survey.customer_account)
    city = django_filters.CharFilter(label=_('Site City'), action=FilterActions.Survey.site_city)
    address = django_filters.CharFilter(label=_('Site Address'), action=FilterActions.Survey.site_address)
    service_type = django_filters.ChoiceFilter(choices=FilterChoices.service_type(), label=_('Service Type'))
    survey_date = django_filters.DateRangeFilter(label=_('Survey Date'))
    survey_type = django_filters.ChoiceFilter(choices=FilterChoices.survey_type(), label=_('Survey Type'))
    surveyor = django_filters.ChoiceFilter(choices=FilterChoices.surveyor(), label=_('Surveyor'),
                                           action=FilterActions.Survey.surveyor)

    class Meta:
        models = models.Survey
        fields = [
            'site',
            'service_type',
            'survey_date',
            'survey_type',
            'surveyor'
        ]