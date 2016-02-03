import django_filters
import models
from django import forms
from django.utils.translation import ugettext as _
from main.parameters import Groups, BP_TYPE_CHOICES, STATES_FILTER, ASSEMBLY_STATUS_CHOICES


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
        for site_use in models.SiteUse.objects.all():
            choices.append((site_use.pk, site_use.site_use))
        return choices

    @staticmethod
    def site_type():
        choices = [('', _('All'))]
        for site_type in models.SiteType.objects.all():
            choices.append((site_type.pk, site_type.site_type))
        return choices

    @staticmethod
    def pws():
        choices = [('', _('All'))]
        for pws in models.PWS.objects.all():
            choices.append((pws.pk, pws.number))
        return choices

    @staticmethod
    def customer_code():
        choices = [('', _('All'))]
        for customer_code in models.CustomerCode.objects.all():
            choices.append((customer_code.pk, customer_code.customer_code))
        return choices

    @staticmethod
    def service_type():
        choices = [('', _('All'))]
        for service_type in models.ServiceType.objects.all():
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
        choices = (('', _('All')), ('none', _('Blank'))) + BP_TYPE_CHOICES
        return choices

    @staticmethod
    def bp_type_test():
        choices = (('', _('All')),) + BP_TYPE_CHOICES
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
        choices = [('', _('All')), ('none', _('Blank'))]
        for assembly_status in ASSEMBLY_STATUS_CHOICES:
            choices.append(assembly_status)
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

    @staticmethod
    def letter_type():
        choices = [('', _('All'))]
        for letter_type in models.LetterType.objects.filter(pws=None):
            choices.append((letter_type.pk, letter_type.letter_type))
        return choices


class FilterActions(object):
    class Site(object):
        @staticmethod
        def next_survey_from(sites, value):
            if value:
                return sites.filter(next_survey_date__gte=value)
            return sites

        @staticmethod
        def next_survey_to(sites, value):
            if value:
                return sites.filter(next_survey_date__lte=value)
            return sites

        @staticmethod
        def last_survey_from(sites, value):
            if value:
                return sites.filter(last_survey_date__gte=value)
            return sites

        @staticmethod
        def last_survey_to(sites, value):
            if value:
                return sites.filter(last_survey_date__lte=value)
            return sites

        @staticmethod
        def next_test_from(sites, value):
            if value:
                return sites.filter(due_install_test_date__gte=value)
            return sites

        @staticmethod
        def next_test_to(sites, value):
            if value:
                return sites.filter(due_install_test_date__lte=value)
            return sites

        @staticmethod
        def connect_date_from(sites, value):
            if value:
                return sites.filter(connect_date__gte=value)
            return sites

        @staticmethod
        def connect_date_to(sites, value):
            if value:
                return sites.filter(connect_date__lte=value)
            return sites

        @staticmethod
        def state(sites, value):
            if value:
                if value == 'blank':
                    return sites.filter(state=None)
                return sites.filter(state=value)
            return sites

        @staticmethod
        def cust_state(sites, value):
            if value:
                if value == 'blank':
                    return sites.filter(cust_state=None)
                return sites.filter(cust_state=value)
            return sites

        @staticmethod
        def street_number_blank(sites, value):
            if value:
                return sites.filter(street_number__isnull=True) | sites.filter(street_number='')
            return sites

        @staticmethod
        def address2_blank(sites, value):
            if value:
                return sites.filter(address2__isnull=True) | sites.filter(address2='')
            return sites

        @staticmethod
        def apt_blank(sites, value):
            if value:
                return sites.filter(apt__isnull=True) | sites.filter(apt='')
            return sites

        @staticmethod
        def zip_blank(sites, value):
            if value:
                return sites.filter(zip__isnull=True) | sites.filter(zip='')
            return sites

        @staticmethod
        def cust_address1_blank(sites, value):
            if value:
                return sites.filter(cust_address1__isnull=True) | sites.filter(cust_address1='')
            return sites

        @staticmethod
        def cust_address2_blank(sites, value):
            if value:
                return sites.filter(cust_address2__isnull=True) | sites.filter(cust_address2='')
            return sites

        @staticmethod
        def cust_apt_blank(sites, value):
            if value:
                return sites.filter(cust_apt__isnull=True) | sites.filter(cust_apt='')
            return sites

        @staticmethod
        def cust_city_blank(sites, value):
            if value:
                return sites.filter(cust_city__isnull=True) | sites.filter(cust_city='')
            return sites

        @staticmethod
        def cust_zip_blank(sites, value):
            if value:
                return sites.filter(cust_zip__isnull=True) | sites.filter(cust_zip='')
            return sites

        @staticmethod
        def route_blank(sites, value):
            if value:
                return sites.filter(route__isnull=True) | sites.filter(route='')
            return sites

        @staticmethod
        def meter_number_blank(sites, value):
            if value:
                return sites.filter(meter_number__isnull=True) | sites.filter(meter_number='')
            return sites

        @staticmethod
        def meter_size_blank(sites, value):
            if value:
                return sites.filter(meter_size__isnull=True) | sites.filter(meter_size='')
            return sites

        @staticmethod
        def meter_reading_blank(sites, value):
            if value:
                return sites.filter(meter_reading__isnull=True) | sites.filter(meter_reading=0.0)
            return sites

        @staticmethod
        def connect_date_blank(sites, value):
            if value:
                return sites.filter(connect_date__isnull=True)
            return sites

        @staticmethod
        def next_survey_blank(sites, value):
            if value:
                return sites.filter(next_survey_date__isnull=True)
            return sites

        @staticmethod
        def last_survey_blank(sites, value):
            if value:
                return sites.filter(last_survey_date__isnull=True)
            return sites

        @staticmethod
        def next_test_blank(sites, value):
            if value:
                return sites.filter(due_install_test_date__isnull=True)
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
                return surveys.filter(site__cust_number__iexact=value)
            return surveys

        @staticmethod
        def site_address(surveys, value):
            if value:
                return surveys.filter(site__address1__icontains=value)
            return surveys

        @staticmethod
        def date_from(surveys, value):
            if value:
                return surveys.filter(survey_date__gte=value)
            return surveys

        @staticmethod
        def date_to(surveys, value):
            if value:
                return surveys.filter(survey_date__lte=value)

    class Test(object):
        @staticmethod
        def pws(tests, value):
            if value:
                return tests.filter(bp_device__hazard__site__pws__id=value)
            return tests

        @staticmethod
        def site_city(tests, value):
            if value:
                return tests.filter(bp_device__hazard__site__city__icontains=value)
            return tests

        @staticmethod
        def customer_account(tests, value):
            if value:
                return tests.filter(bp_device__hazard__site__cust_number__iexact=value)
            return tests

        @staticmethod
        def site_address(tests, value):
            if value:
                return tests.filter(bp_device__hazard__site__address1__icontains=value)
            return tests

        @staticmethod
        def service_type(tests, value):
            if value:
                return tests.filter(bp_device__hazard__service_type__id=value)
            return tests

        @staticmethod
        def hazard_type(tests, value):
            if value:
                return tests.filter(bp_device__hazard__hazard_type__id=value)
            return tests

        @staticmethod
        def bp_type(tests, value):
            if value:
                return tests.filter(bp_device__bp_type_present=value)
            return tests

        @staticmethod
        def test_result(tests, value):
            if value != '':
                return tests.filter(test_result=value)
            return tests

        @staticmethod
        def date_from(tests, value):
            if value:
                return tests.filter(test_date__gte=value)
            return tests

        @staticmethod
        def date_to(tests, value):
            if value:
                return tests.filter(test_date__lte=value)
            return tests

    class Hazard(object):
        @staticmethod
        def due_test_date_from(hazards, value):
            if value:
                return hazards.filter(bp_device__due_test_date__gte=value)
            return hazards

        @staticmethod
        def due_test_date_to(hazards, value):
            if value:
                return hazards.filter(bp_device__due_test_date__lte=value)
            return hazards

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
                return hazards.filter(site__cust_number__icontains=value)
            return hazards

        @staticmethod
        def site_address(hazards, value):
            if value:
                return hazards.filter(site__address1__icontains=value)
            return hazards

        @staticmethod
        def bp_type_present(hazards, value):
            if value:
                if value == 'none':
                    return hazards.filter(bp_type_present=None)
                return hazards.filter(bp_device__bp_type_present=value)
            return hazards

        @staticmethod
        def bp_type_required(hazards, value):
            if value:
                if value == 'none':
                    return hazards.filter(bp_type_required=None)
                return hazards.filter(bp_type_required=value)
            return hazards

        @staticmethod
        def assembly_status(hazards, value):
            if value:
                if value == 'none':
                    return hazards.filter(assembly_status=None)
                return hazards.filter(assembly_status=value)
            return hazards

        @staticmethod
        def due_test_blank(hazards, value):
            if value:
                return hazards.filter(bp_device__due_test_date=None)
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
                return testers.filter(certs__cert_number__icontains=value)
            return testers

        @staticmethod
        def test_serial(testers, value):
            if value:
                return testers.filter(kits__test_serial__icontains=value)
            return testers

    class Letter(object):
        @staticmethod
        def pws(letters, value):
            if value:
                return letters.filter(site__pws__pk=value)
            return letters

        @staticmethod
        def customer(letters, value):
            if value:
                return letters.filter(site__cust_number__icontains=value)
            return letters

        @staticmethod
        def customer_email(letters, value):
            if value:
                return letters.filter(site__contact_email__icontains=value)
            return letters

        @staticmethod
        def service_type(letters, value):
            if value:
                return letters.filter(hazard__service_type__pk=value)
            return letters

        @staticmethod
        def hazard_type(letters, value):
            if value:
                return letters.filter(hazard__hazard_type__pk=value)
            return letters

        @staticmethod
        def letter_type(letters, value):
            if value:
                letter_type = models.LetterType.objects.get(pk=value)
                letter_types_with_same_name = models.LetterType.objects.filter(letter_type=letter_type.letter_type)
                return letters.filter(letter_type__in=letter_types_with_same_name)
            return letters

        @staticmethod
        def user(letters, value):
            if value:
                return letters.filter(user__username__icontains=value)
            return letters

        @staticmethod
        def date_gt(letters, value):
            if value:
                return letters.filter(date__gte=value)
            return letters

        @staticmethod
        def date_lt(letters, value):
            if value:
                return letters.filter(date__lte=value)
            return letters

        @staticmethod
        def bp_type_present(letters, value):
            if value:
                if value == 'none':
                    return letters.filter(hazard__bp_device__bp_type_present=None)
                return letters.filter(hazard__bp_device__bp_type_present=value)
            return letters

        @staticmethod
        def bp_type_required(letters, value):
            if value:
                if value == 'none':
                    return letters.filter(hazard__bp_type_required=None)
                return letters.filter(hazard__bp_type_required=value)
            return letters


class SiteFilter(django_filters.FilterSet):
    pws = django_filters.ChoiceFilter(choices=FilterChoices.pws(), label=_('PWS'))
    cust_number = django_filters.CharFilter(lookup_type='icontains', label=_('Account Number'), name='cust_number')
    cust_code = django_filters.ChoiceFilter(choices=FilterChoices.customer_code(), label=_('Customer Code'),
                                            name='cust_code')
    cust_name = django_filters.CharFilter(lookup_type='icontains', label=_('Customer Name'), name='cust_name')
    street_number = django_filters.CharFilter(lookup_type='icontains', label=_('Street Number'), name='street_number')
    address1 = django_filters.CharFilter(lookup_type='icontains', label=_('Service Address 1'), name='address1')
    address2 = django_filters.CharFilter(lookup_type='icontains', label=_('Service Address 2'), name='address2')
    apt = django_filters.CharFilter(lookup_type='icontains', label=_('Service Apt'))
    city = django_filters.CharFilter(lookup_type='icontains', label=_('Service City'))
    state = django_filters.ChoiceFilter(choices=STATES_FILTER, label=_('Service State'),
                                        action=FilterActions.Site.state)
    zip = django_filters.CharFilter(lookup_type='icontains', label=_('Service ZIP'))
    cust_address1 = django_filters.CharFilter(lookup_type='icontains', label=_('Customer Address 1'))
    cust_address2 = django_filters.CharFilter(lookup_type='icontains', label=_('Customer Address 2'))
    cust_apt = django_filters.CharFilter(lookup_type='icontains', label=_('Customer Apt'))
    cust_city = django_filters.CharFilter(lookup_type='icontains', label=_('Customer City'))
    cust_state = django_filters.ChoiceFilter(choices=STATES_FILTER, label=_('Customer State'),
                                             action=FilterActions.Site.cust_state)
    cust_zip = django_filters.CharFilter(lookup_type='icontains', label=_('Customer ZIP'))

    next_survey_from = django_filters.DateFilter(action=FilterActions.Site.next_survey_from,
                                                 label=_('Next Survey From'))
    next_survey_to = django_filters.DateFilter(action=FilterActions.Site.next_survey_to, label=_('Next Survey To'))
    next_survey_blank = django_filters.BooleanFilter(action=FilterActions.Site.next_survey_blank,
                                                     widget=forms.CheckboxInput, label="Next Survey Blank")
    last_survey_from = django_filters.DateFilter(action=FilterActions.Site.last_survey_from,
                                                 label=_('Last Survey From'))
    last_survey_to = django_filters.DateFilter(action=FilterActions.Site.last_survey_to, label=_('Last Survey To'))
    last_survey_blank = django_filters.BooleanFilter(action=FilterActions.Site.last_survey_blank,
                                                     widget=forms.CheckboxInput, label="Last Survey Blank")
    due_test_from = django_filters.DateFilter(action=FilterActions.Site.next_test_from, label=_('Due Test From'))
    due_test_to = django_filters.DateFilter(action=FilterActions.Site.next_test_to, label=_('Due Test To'))
    due_test_blank = django_filters.BooleanFilter(action=FilterActions.Site.next_test_blank,
                                                  widget=forms.CheckboxInput, label="Due Test Blank")
    route = django_filters.CharFilter(label=_('Seq. Route'), lookup_type='icontains')
    meter_number = django_filters.CharFilter(lookup_type='icontains', label=_('Meter Number'))
    meter_size = django_filters.CharFilter(lookup_type='icontains', label=_('Meter Size'))
    meter_reading = django_filters.NumberFilter(label=_('Meter Reading'))
    connect_date_from = django_filters.DateFilter(label=_('Connect Date'), action=FilterActions.Site.connect_date_from)
    connect_date_to = django_filters.DateFilter(label=_('Connect Date'), action=FilterActions.Site.connect_date_to)
    street_number_blank = django_filters.BooleanFilter(action=FilterActions.Site.street_number_blank,
                                                       widget=forms.CheckboxInput)
    address2_blank = django_filters.BooleanFilter(action=FilterActions.Site.address2_blank,
                                                  widget=forms.CheckboxInput)
    apt_blank = django_filters.BooleanFilter(action=FilterActions.Site.apt_blank,
                                             widget=forms.CheckboxInput)
    zip_blank = django_filters.BooleanFilter(action=FilterActions.Site.zip_blank,
                                             widget=forms.CheckboxInput)
    cust_address1_blank = django_filters.BooleanFilter(action=FilterActions.Site.cust_address1_blank,
                                                       widget=forms.CheckboxInput)
    cust_address2_blank = django_filters.BooleanFilter(action=FilterActions.Site.cust_address2_blank,
                                                       widget=forms.CheckboxInput)
    cust_apt_blank = django_filters.BooleanFilter(action=FilterActions.Site.cust_apt_blank,
                                                  widget=forms.CheckboxInput)
    cust_city_blank = django_filters.BooleanFilter(action=FilterActions.Site.cust_city_blank,
                                                   widget=forms.CheckboxInput)
    cust_zip_blank = django_filters.BooleanFilter(action=FilterActions.Site.cust_zip_blank,
                                                  widget=forms.CheckboxInput)
    route_blank = django_filters.BooleanFilter(action=FilterActions.Site.route_blank,
                                               widget=forms.CheckboxInput)
    meter_number_blank = django_filters.BooleanFilter(action=FilterActions.Site.meter_number_blank,
                                                      widget=forms.CheckboxInput)
    meter_size_blank = django_filters.BooleanFilter(action=FilterActions.Site.meter_size_blank,
                                                    widget=forms.CheckboxInput)
    meter_reading_blank = django_filters.BooleanFilter(action=FilterActions.Site.meter_reading_blank,
                                                       widget=forms.CheckboxInput)
    connect_date_blank = django_filters.BooleanFilter(action=FilterActions.Site.connect_date_blank,
                                                      widget=forms.CheckboxInput)

    # they aren't displayed currently but may require them later
    # site_type = django_filters.ChoiceFilter(choices=FilterChoices.site_type(), label=_('Site Type'))
    # site_use = django_filters.ChoiceFilter(choices=FilterChoices.site_use(), label=_('Site Use'))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)

        super(SiteFilter, self).__init__(*args, **kwargs)
        if user and not user.is_superuser:
            choices = [('', 'All')] + [(pws.pk, pws) for pws in user.employee.pws.all()]
            self.filters['pws'].field.choices = choices


class SurveyFilter(django_filters.FilterSet):
    pws = django_filters.ChoiceFilter(choices=FilterChoices.pws(), label=_('PWS'), action=FilterActions.Survey.pws)
    customer = django_filters.CharFilter(label=_('Customer Account'), action=FilterActions.Survey.customer_account)
    city = django_filters.CharFilter(label=_('Site City'), action=FilterActions.Survey.site_city)
    address = django_filters.CharFilter(label=_('Service Address'), action=FilterActions.Survey.site_address)
    service_type = django_filters.ChoiceFilter(choices=FilterChoices.service_type(), label=_('Service Type'))
    survey_date_from = django_filters.DateFilter(label=_('Survey Date From'), action=FilterActions.Survey.date_from)
    survey_date_to = django_filters.DateFilter(label=_('Survey Date To'), action=FilterActions.Survey.date_to)
    survey_type = django_filters.ChoiceFilter(choices=FilterChoices.survey_type(), label=_('Survey Type'))
    surveyor = django_filters.ChoiceFilter(choices=FilterChoices.surveyor(), label=_('Surveyor'))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)

        super(SurveyFilter, self).__init__(*args, **kwargs)
        if user and not user.is_superuser:
            choices = [('', 'All')] + [(pws.pk, pws) for pws in user.employee.pws.all()]
            self.filters['pws'].field.choices = choices


class TestFilter(django_filters.FilterSet):
    pws = django_filters.ChoiceFilter(choices=FilterChoices.pws(), label=_('PWS'), action=FilterActions.Test.pws)
    customer = django_filters.CharFilter(label=_('Customer Account'), action=FilterActions.Test.customer_account)
    city = django_filters.CharFilter(label=_('Site City'), action=FilterActions.Test.site_city)
    address = django_filters.CharFilter(label=_('Service Address'), action=FilterActions.Test.site_address)
    service_type = django_filters.ChoiceFilter(choices=FilterChoices.service_type(), label=_('Service Type'),
                                               action=FilterActions.Test.service_type)
    hazard_type = django_filters.ChoiceFilter(choices=FilterChoices.hazard_type(), label=_('Hazard Type'),
                                              action=FilterActions.Test.hazard_type)
    bp_type = django_filters.ChoiceFilter(choices=FilterChoices.bp_type_test(), label=_('BP Type Present'),
                                          action=FilterActions.Test.bp_type)
    test_date_from = django_filters.DateFilter(label=_('Test Date From'), action=FilterActions.Test.date_from)
    test_date_to = django_filters.DateFilter(label=_('Test Date To'), action=FilterActions.Test.date_to)
    tester = django_filters.ChoiceFilter(choices=FilterChoices.tester(), label=_('Tester'))
    test_result = django_filters.ChoiceFilter(choices=FilterChoices.test_result(), label=_('Test Result'),
                                              action=FilterActions.Test.test_result)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)

        super(TestFilter, self).__init__(*args, **kwargs)
        if user and not user.is_superuser:
            choices = [('', 'All')] + [(pws.pk, pws) for pws in user.employee.pws.all()]
            self.filters['pws'].field.choices = choices


class HazardFilter(django_filters.FilterSet):
    pws = django_filters.ChoiceFilter(choices=FilterChoices.pws(), label=_('PWS'), action=FilterActions.Hazard.pws)
    customer = django_filters.CharFilter(label=_('Customer Account'), action=FilterActions.Hazard.customer_account)
    city = django_filters.CharFilter(label=_('Site City'), action=FilterActions.Hazard.site_city)
    address = django_filters.CharFilter(label=_('Service Address'), action=FilterActions.Hazard.site_address)
    service_type = django_filters.ChoiceFilter(choices=FilterChoices.service_type(), label=_('Service Type'))
    hazard_type = django_filters.ChoiceFilter(choices=FilterChoices.hazard_type(), label=_('Hazard Type'))
    assembly_status = django_filters.ChoiceFilter(choices=FilterChoices.assembly_status(), label=_('Assembly Status'),
                                                  action=FilterActions.Hazard.assembly_status)
    bp_type_present = django_filters.ChoiceFilter(choices=FilterChoices.bp_type(), label=_('BP Type Present'),
                                                  action=FilterActions.Hazard.bp_type_present)
    bp_type_required = django_filters.ChoiceFilter(choices=FilterChoices.bp_type(), label=_('BP Type Required'),
                                                   action=FilterActions.Hazard.bp_type_required)
    due_test_date_from = django_filters.DateFilter(label=_('Test Due Date From'),
                                                   action=FilterActions.Hazard.due_test_date_from)
    due_test_date_to = django_filters.DateFilter(label=_("Test Due Date To"),
                                                 action=FilterActions.Hazard.due_test_date_to)
    due_test_blank = django_filters.BooleanFilter(action=FilterActions.Hazard.due_test_blank,
                                                  widget=forms.CheckboxInput, label="Test Due Date Blank")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)

        super(HazardFilter, self).__init__(*args, **kwargs)
        if user and not user.is_superuser:
            choices = [('', 'All')] + [(pws.pk, pws) for pws in user.employee.pws.all()]
            self.filters['pws'].field.choices = choices


class TesterFilter(django_filters.FilterSet):
    pws = django_filters.ChoiceFilter(choices=FilterChoices.pws(), label=_('PWS'), action=FilterActions.User.pws)
    username = django_filters.CharFilter(label=_('Username'), lookup_type="icontains")
    name = django_filters.CharFilter(label=_('Name or Surname'), action=FilterActions.User.name)
    company = django_filters.CharFilter(label=_('Company'), action=FilterActions.User.company)
    email = django_filters.CharFilter(label=_('Email'), lookup_type='icontains')
    cert_number = django_filters.CharFilter(label=_('Certificate Number'), action=FilterActions.User.cert_number)
    test_serial = django_filters.CharFilter(label=_('Test Kit Serial'), action=FilterActions.User.test_serial)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)

        super(TesterFilter, self).__init__(*args, **kwargs)
        if user and not user.is_superuser:
            choices = [('', 'All')] + [(pws.pk, pws) for pws in user.employee.pws.all()]
            self.filters['pws'].field.choices = choices


class LetterFilter(django_filters.FilterSet):
    pws = django_filters.ChoiceFilter(label=_("PWS"), choices=FilterChoices.pws(),
                                      action=FilterActions.Letter.pws)
    customer = django_filters.CharFilter(label=_("Customer Account"), action=FilterActions.Letter.customer)
    customer_email = django_filters.CharFilter(label=_("Customer Email"), action=FilterActions.Letter.customer_email)
    service_type = django_filters.ChoiceFilter(label=_("Service Type"), choices=FilterChoices.service_type(),
                                               action=FilterActions.Letter.service_type)
    hazard_type = django_filters.ChoiceFilter(label=_("Hazard Type"), choices=FilterChoices.hazard_type(),
                                              action=FilterActions.Letter.hazard_type)
    letter_type = django_filters.ChoiceFilter(label=_("Letter Type"), choices=FilterChoices.letter_type(),
                                              action=FilterActions.Letter.letter_type)
    user = django_filters.CharFilter(label=_("Username"), action=FilterActions.Letter.user)
    already_sent = django_filters.BooleanFilter(label=_("Already Sent"))
    date_gt = django_filters.DateFilter(label=_("Letter Date From"), action=FilterActions.Letter.date_gt)
    date_lt = django_filters.DateFilter(label=_("Letter Date To"), action=FilterActions.Letter.date_lt)
    bp_type_present = django_filters.ChoiceFilter(choices=FilterChoices.bp_type(), label=_('Assembly Type present'),
                                                  action=FilterActions.Letter.bp_type_present)
    bp_type_required = django_filters.ChoiceFilter(choices=FilterChoices.bp_type(), label=_('Assembly Type required'),
                                                   action=FilterActions.Letter.bp_type_required)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)

        super(LetterFilter, self).__init__(*args, **kwargs)
        if user and not user.is_superuser:
            choices = [('', 'All')] + [(pws.pk, pws) for pws in user.employee.pws.all()]
            self.filters['pws'].field.choices = choices
