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
        surveyors = models.User.objects.filter(groups__name=Groups.surveyor).order_by('username')
        for user in surveyors:
            choices.append((user.pk, user.username))
        return choices

    @staticmethod
    def survey_type():
        choices = [('', _('All'))]
        for survey_type in models.SurveyType.objects.all():
            choices.append((survey_type.pk, survey_type.survey_type))
        return choices

    @staticmethod
    def hazard_type():
        choices = [('', _('All'))]
        for hazard_type in models.HazardType.objects.all():
            choices.append((hazard_type.pk, hazard_type.hazard_type))
        return choices

    @staticmethod
    def bp_type():
        choices = [('', _('All'))]
        for bp_type in models.BPType.objects.all():
            choices.append((bp_type.pk, bp_type.bp_type))
        return choices

    @staticmethod
    def tester():
        choices = [('', _('All'))]
        testers = models.User.objects.filter(groups__name=Groups.tester).order_by('username')
        for user in testers:
            choices.append((user.pk, user.username))
        return choices

    @staticmethod
    def test_result():
        return [('', _('All')), (1, _('Passed')), (0, _('Failed'))]

    @staticmethod
    def assembly_status():
        choices = [('', _('All'))]
        for assembly_status in models.AssemblyStatus.objects.all():
            choices.append((assembly_status.pk, assembly_status.assembly_status))
        return choices

    @staticmethod
    def test_manufacturer():
        choices = [('', _('All'))]
        for test_manufacturer in models.TestManufacturer.objects.all():
            choices.append((test_manufacturer.pk, test_manufacturer.test_manufacturer))
        return choices

    @staticmethod
    def test_model():
        choices = [('', _('All'))]
        for model in models.TestModel.objects.all():
            choices.append((model.pk, model.model))
        return choices

    @staticmethod
    def yesno():
        return [('', _('All')), (1, _('Yes')), (0, _('No'))]


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
        def site_address(surveys, value):
            if value:
                return surveys.filter(site__address1__icontains=value)
            return surveys

    class Test(object):
        @staticmethod
        def pws(tests, value):
            if value:
                return tests.filter(bp_device__site__pws__id=value)
            return tests

        @staticmethod
        def site_city(tests, value):
            if value:
                return tests.filter(bp_device__site__city__icontains=value)
            return tests

        @staticmethod
        def customer_account(tests, value):
            if value:
                return tests.filter(bp_device__site__customer__number__icontains=value)
            return tests

        @staticmethod
        def site_address(tests, value):
            if value:
                return tests.filter(bp_device__site__address1__icontains=value)
            return tests

        @staticmethod
        def service_type(tests, value):
            if value:
                return tests.filter(bp_device__service_type__id=value)
            return tests

        @staticmethod
        def hazard_type(tests, value):
            if value:
                return tests.filter(bp_device__hazard_type__id=value)
            return tests

        @staticmethod
        def bp_type(tests, value):
            if value:
                return tests.filter(bp_device__bp_type_present__id=value)
            return tests

        @staticmethod
        def test_result(tests, value):
            if value != '':
                return tests.filter(test_result=value)
            return tests

    class Hazard(object):
        @staticmethod
        def pws(hazards, value):
            if value:
                return hazards.filter(site__pws__id=value)
            return hazards

        @staticmethod
        def site_city(hazards, value):
            if value:
                return hazards.filter(site__city__icontains=value)
            return hazards

        @staticmethod
        def customer_account(hazards, value):
            if value:
                return hazards.filter(site__customer__number__icontains=value)
            return hazards

        @staticmethod
        def site_address(hazards, value):
            if value:
                return hazards.filter(site__address1__icontains=value)
            return hazards

    class User(object):
        @staticmethod
        def pws(testers, value):
            if value:
                return testers.filter(employee__pws=value)
            return testers

        @staticmethod
        def name(testers, value):
            if value:
                return testers.filter(first_name__icontains=value) | testers.filter(last_name__icontains=value)
            return testers

        @staticmethod
        def company(testers, value):
            if value:
                return testers.filter(employee__company__icontains=value)
            return testers

        @staticmethod
        def cert_number(testers, value):
            if value:
                return testers.filter(employee__cert_number__icontains=value)
            return testers

        @staticmethod
        def cert_active(testers, value):
            if value != '':
                current_date = datetime.now().date()
                certified_testers = testers.filter(employee__cert_expires__gte=current_date,
                                                   employee__cert_date__lte=current_date)
                if value:
                    return certified_testers
                else:
                    return testers.exclude(id__in=certified_testers)
            return testers

        @staticmethod
        def test_manufacturer(testers, value):
            if value:
                return testers.filter(employee__test_manufacturer=value)
            return testers

        @staticmethod
        def test_model(testers, value):
            if value:
                return testers.filter(employee__test_model=value)
            return testers

        @staticmethod
        def test_serial(testers, value):
            if value:
                return testers.filter(employee__test_serial__icontains=value)
            return testers

        @staticmethod
        def test_last_cert(testers, value):
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
                return testers.filter(employee__test_last_cert=None)
            if value in dates:
                return testers.filter(employee__test_last_cert__gt=dates[value])
            return testers


class SiteFilter(django_filters.FilterSet):
    pws = django_filters.ChoiceFilter(choices=FilterChoices.pws(), label=_('PWS'))
    customer_name = django_filters.CharFilter(label=_('Customer Name'),
                                              action=FilterActions.Site.customer_name)
    customer_account = django_filters.CharFilter(label=_('Customer Account'),
                                                 action=FilterActions.Site.customer_account)
    city = django_filters.CharFilter(lookup_type='icontains', label=_('Site City'))
    address = django_filters.CharFilter(lookup_type='icontains', label=_('Service Address'), name='address1')
    site_type = django_filters.ChoiceFilter(choices=FilterChoices.site_type(), label=_('Site Type'))
    site_use = django_filters.ChoiceFilter(choices=FilterChoices.site_use(), label=_('Site Use'))
    status = django_filters.ChoiceFilter(choices=FilterChoices.site_status(), label=_('Site Status'))
    next_survey_date = django_filters.ChoiceFilter(choices=NEXT_DATE_FILTER_CHOICES,
                                                   action=FilterActions.Site.next_date,
                                                   label=_('Next Survey Date'))
    last_survey_date = django_filters.ChoiceFilter(choices=PAST_DATE_FILTER_CHOICES,
                                                   action=FilterActions.Site.last_date,
                                                   label=_('Last Survey older than'))
    route = django_filters.CharFilter(label=_('Seq. Route'), lookup_type='exact')


class CustomerFilter(django_filters.FilterSet):
    number = django_filters.CharFilter(label=_('Account Number'), lookup_type='icontains')
    name = django_filters.CharFilter(label=_('Customer Name'), lookup_type='icontains')
    code = django_filters.ChoiceFilter(label=_('Customer Code'), choices=FilterChoices.customer_code())
    city = django_filters.CharFilter(label=_('City'), lookup_type='icontains')
    address = django_filters.CharFilter(label=_('Address'), lookup_type='icontains', name='address1')
    zip = django_filters.CharFilter(label=_('ZIP'), lookup_type='icontains')


class SurveyFilter(django_filters.FilterSet):
    pws = django_filters.ChoiceFilter(choices=FilterChoices.pws(), label=_('PWS'), action=FilterActions.Survey.pws)
    customer = django_filters.CharFilter(label=_('Customer Account'), action=FilterActions.Survey.customer_account)
    city = django_filters.CharFilter(label=_('Site City'), action=FilterActions.Survey.site_city)
    address = django_filters.CharFilter(label=_('Service Address'), action=FilterActions.Survey.site_address)
    service_type = django_filters.ChoiceFilter(choices=FilterChoices.service_type(), label=_('Service Type'))
    survey_date = django_filters.DateRangeFilter(label=_('Survey Date'))
    survey_type = django_filters.ChoiceFilter(choices=FilterChoices.survey_type(), label=_('Survey Type'))
    surveyor = django_filters.ChoiceFilter(choices=FilterChoices.surveyor(), label=_('Surveyor'))


class TestFilter(django_filters.FilterSet):
    pws = django_filters.ChoiceFilter(choices=FilterChoices.pws(), label=_('PWS'), action=FilterActions.Test.pws)
    customer = django_filters.CharFilter(label=_('Customer Account'), action=FilterActions.Test.customer_account)
    city = django_filters.CharFilter(label=_('Site City'), action=FilterActions.Test.site_city)
    address = django_filters.CharFilter(label=_('Service Address'), action=FilterActions.Test.site_address)
    service_type = django_filters.ChoiceFilter(choices=FilterChoices.service_type(), label=_('Service Type'),
                                               action=FilterActions.Test.service_type)
    hazard_type = django_filters.ChoiceFilter(choices=FilterChoices.hazard_type(), label=_('Hazard Type'),
                                              action=FilterActions.Test.hazard_type)
    bp_type = django_filters.ChoiceFilter(choices=FilterChoices.bp_type(), label=_('BP Type Present'),
                                          action=FilterActions.Test.bp_type)
    test_date = django_filters.DateRangeFilter(label=_('Test Date'))
    tester = django_filters.ChoiceFilter(choices=FilterChoices.tester(), label=_('Tester'))
    test_result = django_filters.ChoiceFilter(choices=FilterChoices.test_result(), label=_('Test Result'),
                                              action=FilterActions.Test.test_result)


class HazardFilter(django_filters.FilterSet):
    pws = django_filters.ChoiceFilter(choices=FilterChoices.pws(), label=_('PWS'), action=FilterActions.Hazard.pws)
    customer = django_filters.CharFilter(label=_('Customer Account'), action=FilterActions.Hazard.customer_account)
    city = django_filters.CharFilter(label=_('Site City'), action=FilterActions.Hazard.site_city)
    address = django_filters.CharFilter(label=_('Service Address'), action=FilterActions.Hazard.site_address)
    service_type = django_filters.ChoiceFilter(choices=FilterChoices.service_type(), label=_('Service Type'))
    hazard_type = django_filters.ChoiceFilter(choices=FilterChoices.hazard_type(), label=_('Hazard Type'))
    assembly_status = django_filters.ChoiceFilter(choices=FilterChoices.assembly_status(), label=_('Assembly Status'))
    bp_type_present = django_filters.ChoiceFilter(choices=FilterChoices.bp_type(), label=_('BP Type Present'))
    due_install_test_date = django_filters.DateRangeFilter(label=_('Due Install/Test Date'))


class TesterFilter(django_filters.FilterSet):
    pws = django_filters.ChoiceFilter(choices=FilterChoices.pws(), label=_('PWS'), action=FilterActions.User.pws)
    username = django_filters.CharFilter(label=_('Username'), lookup_type="icontains")
    name = django_filters.CharFilter(label=_('Name or Surname'), action=FilterActions.User.name)
    company = django_filters.CharFilter(label=_('Company'), action=FilterActions.User.company)
    cert_number = django_filters.CharFilter(label=_('Certificate Number'), action=FilterActions.User.cert_number)
    cert_active = django_filters.ChoiceFilter(label=_('Certificate Active'), choices=FilterChoices.yesno(),
                                              action=FilterActions.User.cert_active)
    test_manufacturer = django_filters.ChoiceFilter(label=_('Test Manufacturer'),
                                                    choices=FilterChoices.test_manufacturer(),
                                                    action=FilterActions.User.test_manufacturer)
    test_model = django_filters.ChoiceFilter(label=_('Test Model'), choices=FilterChoices.test_model(),
                                             action=FilterActions.User.test_model)
    test_serial = django_filters.CharFilter(label=_('Test Kit Serial'), action=FilterActions.User.test_serial)
    test_last_cert = django_filters.ChoiceFilter(label=_('Test Kit Last Calibrated'),
                                                 choices=PAST_DATE_FILTER_CHOICES,
                                                 action=FilterActions.User.test_last_cert)