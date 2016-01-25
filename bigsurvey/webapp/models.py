from decimal import Decimal
from datetime import date

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User, Group
from ckeditor.fields import RichTextField
from reversion import revisions as reversion

from main.parameters import *
from utils import photo_util
import fields

import uuid


class SourceType(models.Model):
    source_type = models.CharField(max_length=50, verbose_name=_("Source Type"))

    def __unicode__(self):
        return u"%s" % self.source_type

    class Meta:
        verbose_name = _('Source Type')
        verbose_name_plural = _('Source Types')
        ordering = ('source_type',)
        permissions = (
            ('browse_sourcetype', _('Can browse Source Type')),
        )

reversion.register(SourceType)


class SiteType(models.Model):
    site_type = models.CharField(max_length=50, verbose_name=_("Site Type"))

    def __unicode__(self):
        return u"%s" % self.site_type

    class Meta:
        verbose_name = _('Site Type')
        verbose_name_plural = _('Site Types')
        ordering = ('site_type',)
        permissions = (
            ('browse_sitetype', _('Can browse Site Type')),
        )

reversion.register(SiteType)


class SiteUse(models.Model):
    site_use = models.CharField(max_length=30, verbose_name=_("Site Use"))

    def __unicode__(self):
        return u"%s" % self.site_use

    class Meta:
        verbose_name = _('Site Use')
        verbose_name_plural = _('Site Use Types')
        ordering = ('site_use',)
        permissions = (
            ('browse_siteuse', _('Can browse Site Use')),
        )

reversion.register(SiteUse)


class ServiceType(models.Model):
    service_type = models.CharField(max_length=20, verbose_name=_("Service Type"))

    def __unicode__(self):
        return u"%s" % self.service_type

    class Meta:
        verbose_name = _('Service Type')
        verbose_name_plural = _('Service Types')
        ordering = ('service_type',)
        permissions = (
            ('browse_servicetype', _('Can browse Service Type')),
        )

reversion.register(ServiceType)


class SurveyType(models.Model):
    survey_type = models.CharField(max_length=20, verbose_name=_("Survey Type"))

    def __unicode__(self):
        return u"%s" % self.survey_type

    class Meta:
        verbose_name = _('Survey Type')
        verbose_name_plural = _('Survey Types')
        ordering = ('survey_type',)
        permissions = (
            ('browse_surveytype', _('Can browse Survey Type')),
        )

reversion.register(SurveyType)


class BPSize(models.Model):
    bp_size = models.CharField(max_length=10, verbose_name=_("BFP Size"))

    def __unicode__(self):
        return u"%s" % self.bp_size

    class Meta:
        verbose_name = _('BFP Size')
        verbose_name_plural = _('BFP Sizes')
        ordering = ('bp_size',)
        permissions = (
            ('browse_bpsize', _('Can browse BP Size')),
        )


reversion.register(BPSize)


class BPManufacturer(models.Model):
    bp_manufacturer = models.CharField(max_length=30, verbose_name=_("BFP Manufacturer"))

    def __unicode__(self):
        return u"%s" % self.bp_manufacturer

    class Meta:
        verbose_name = _('BFP Manufacturer')
        verbose_name_plural = _('BFP Manufacturers')
        ordering = ('bp_manufacturer',)
        permissions = (
            ('browse_bpmanufacturer', _('Can browse BP Manufacturer')),
        )

reversion.register(BPManufacturer)


class CustomerCode(models.Model):
    customer_code = models.CharField(max_length=20, verbose_name=_("Customer Code"))

    def __unicode__(self):
        return u"%s" % self.customer_code

    class Meta:
        verbose_name = _('Customer Code')
        verbose_name_plural = _('Customer Codes')
        ordering = ('customer_code',)
        permissions = (
            ('browse_customercode', _('Can browse Customer Code')),
        )

reversion.register(CustomerCode)


class HazardType(models.Model):
    hazard_type = models.CharField(max_length=50, verbose_name=_("Hazard Type"))

    def __unicode__(self):
        return u"%s" % self.hazard_type

    class Meta:
        verbose_name = _('Hazard Type')
        verbose_name_plural = _('Hazard Types')
        ordering = ('hazard_type',)
        permissions = (
            ('browse_hazardtype', _('Can browse Hazard Type')),
        )

reversion.register(HazardType)


class TestManufacturer(models.Model):
    test_manufacturer = models.CharField(max_length=20, verbose_name=_("Test Manufacturer"))

    def __unicode__(self):
        return u"%s" % self.test_manufacturer

    class Meta:
        verbose_name = _('Test Manufacturer')
        verbose_name_plural = _('Test Manufacturers')
        ordering = ('test_manufacturer',)
        permissions = (
            ('browse_testmanufacturer', _('Can browse Test Manufacturer')),
        )

reversion.register(TestManufacturer)


class ICPointType(models.Model):
    ic_point = models.CharField(max_length=20, verbose_name=_("Interconnection Point"))

    def __unicode__(self):
        return u"%s" % self.ic_point

    class Meta:
        verbose_name = _('Interconnection Point Type')
        verbose_name_plural = _('Interconnection Point Types')
        ordering = ('ic_point',)
        permissions = (
            ('browse_icpointtype', _('Can browse Interconnection Point Type')),
        )

reversion.register(ICPointType)


class AssemblyLocation(models.Model):
    assembly_location = models.CharField(max_length=20, verbose_name=_("Assembly Location"))

    def __unicode__(self):
        return u"%s" % self.assembly_location

    class Meta:
        verbose_name = _('Assembly Location')
        verbose_name_plural = _('Assembly Locations')
        ordering = ('assembly_location',)
        permissions = (
            ('browse_assemblylocation', _('Can browse Assembly Location')),
        )

reversion.register(AssemblyLocation)


class AssemblyStatus(models.Model):
    assembly_status = models.CharField(max_length=50, verbose_name=_("Assembly Status"))

    def __unicode__(self):
        return u"%s" % self.assembly_status

    class Meta:
        verbose_name = _('Assembly Status')
        verbose_name_plural = _('Assembly Statuses')
        ordering = ('assembly_status',)
        permissions = (
            ('browse_assemblystatus', _('Can browse Assembly Status')),
        )

reversion.register(AssemblyStatus)


class FloorsCount(models.Model):
    floors_count = models.CharField(max_length=10, verbose_name=_("Floors Count"))

    def __unicode__(self):
        return u"%s" % self.floors_count

    class Meta:
        verbose_name = _('Floors Count')
        verbose_name_plural = _('Floors Count')
        ordering = ('floors_count',)
        permissions = (
            ('browse_floorscount', _('Can browse Floors Count')),
        )

reversion.register(FloorsCount)


class TestModel(models.Model):
    model = models.CharField(max_length=20, verbose_name=_("Test Model"))

    def __unicode__(self):
        return u"%s" % self.model

    class Meta:
        verbose_name = _('Test Model')
        verbose_name_plural = _('Test Models')
        ordering = ('model',)
        permissions = (
            ('browse_testmodel', _('Can browse Test Models')),
        )

reversion.register(TestModel)


class Special(models.Model):
    special = models.CharField(max_length=5, verbose_name=_("Special"))

    def __unicode__(self):
        return u"%s" % self.special

    class Meta:
        verbose_name = _('Special')
        verbose_name_plural = _('Special')
        ordering = ('special',)
        permissions = (
            ('browse_special', _('Can browse Special')),
        )

reversion.register(Special)


class Orientation(models.Model):
    orientation = models.CharField(max_length=15, verbose_name=_("Orientation"))

    def __unicode__(self):
        return u"%s" % self.orientation

    class Meta:
        verbose_name = _('Orientation Type')
        verbose_name_plural = _('Orientation Types')
        ordering = ('orientation',)
        permissions = (
            ('browse_orientation', _('Can browse Orientation Type')),
        )

reversion.register(Orientation)


class SiteStatus(models.Model):
    site_status = models.CharField(max_length=15, verbose_name=_("Site Status"))

    def __unicode__(self):
        return u"%s" % self.site_status

    class Meta:
        verbose_name = _('Site Status')
        verbose_name_plural = _('Site Status')
        ordering = ('site_status',)
        permissions = (
            ('browse_sitestatus', _('Can browse Site Status')),
        )

reversion.register(SiteStatus)


class Regulation(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Regulation Type"))

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        verbose_name = _('Regulation Type')
        verbose_name_plural = _('Regulation Types')
        ordering = ('name',)
        permissions = (
            ('browse_regulation', _('Can browse Regulation Type')),
        )

reversion.register(Regulation)


class HazardDegree(models.Model):
    degree = models.CharField(max_length=50, verbose_name=_("Hazard Degree"))

    def __unicode__(self):
        return u"%s" % self.degree

    class Meta:
        verbose_name = _('Hazard Degree')
        verbose_name_plural = _('Hazard Degrees')
        ordering = ('pk',)
        permissions = (
            ('browse_hazard_degree', _('Can browse Hazard Degree')),
        )

reversion.register(HazardDegree)


class PWS(models.Model):
    number = models.CharField(max_length=15, verbose_name=_("Number"))
    name = models.CharField(max_length=50, verbose_name=_("Name"))
    logo = fields.ImageField(upload_to='pws_logos', null=True, blank=True, verbose_name=_("Pws logo"))
    zip = models.CharField(max_length=10, blank=True, null=True, verbose_name=_("ZIP"))
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0), blank=True, verbose_name=_("Test's Price"))
    city = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("City"))
    state = models.CharField(max_length=2, null=True, blank=True, choices=STATES, verbose_name=_("State"), help_text=_("Site's State"))
    office_address = models.CharField(blank=True, null=True, max_length=50, verbose_name=_("Office Address"))
    water_source = models.ForeignKey(SourceType, blank=True, null=True, verbose_name=_("Water Source"), related_name="pws")
    notes = models.TextField(max_length=255, blank=True, null=True, verbose_name=_("Notes"))
    consultant_name = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Consultant Name'))
    consultant_phone = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Consultant Phone'))
    plumber_packet_location = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Plumber Packet Location'))
    plumber_packet_address = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Plumber Packet Address'))
    bailee_name = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Name of Director of Public Works or other person on whose behalf the letter will be sent'))
    bailee_job_title = models.CharField(max_length=100, default='Director of Public Works', verbose_name=_('Job title of person on whose behalf the letter will be sent'))
    phone = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("PWS's Phone number"))
    fax = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("PWS's Fax number"))
    email = models.EmailField(max_length=100, blank=True, null=True, verbose_name=_("PWS's email"))
    letter_left_header_block = RichTextField(blank=True, verbose_name=_('Letter Left Header block'))
    letter_right_header_block = RichTextField(blank=True, verbose_name=_('Letter Right Header block'))

    def __unicode__(self):
        return u"%s, %s" % (self.number, self.name)

    def get_pws_list(self):
        return [self]

    class Meta:
        verbose_name = _('Public Water System')
        verbose_name_plural = _('Public Water Systems')
        ordering = ('number',)
        permissions = (
            ('browse_pws', _('Can browse Public Water System')),
            ('browse_all_pws', _('Can browse all Public Water Systems')),
            ('own_multiple_pws', _('Owns multiple Public Water Systems')),
            ('change_own_pws', _('Can change his own Public Water System'))
        )

reversion.register(PWS)


class LetterType(models.Model):
    letter_type = models.CharField(max_length=20, verbose_name=_("Letter Type"))
    template = RichTextField(blank=False, null=False, default=_('Default Letter Template'), verbose_name=_('Letter Template'))
    header = models.CharField(blank=False, null=False, default=_('Backflow Prevention Services Notification'), verbose_name=_('Letter Header'), max_length=150)
    pws = models.ForeignKey(PWS, null=True, blank=True, default=None, related_name='letter_types')

    def __unicode__(self):
        return u"%s" % self.letter_type

    def get_pws_list(self):
        return [self.pws]

    class Meta:
        verbose_name = _('Letter Type')
        verbose_name_plural = _('Letter Types')
        unique_together = 'letter_type', 'pws'
        ordering = ('letter_type',)
        permissions = (
            ('browse_lettertype', _('Can browse Letter Type')),
            ('access_to_all_lettertypes', _('Has access to all Letter Types')),
            ('access_to_pws_lettertypes', _('Has access to PWS\' Letter Types')),
        )

reversion.register(LetterType)


class Employee(models.Model):
    user = models.OneToOneField(User)
    address = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Address"))
    city = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("City"))
    state = models.CharField(max_length=2, blank=True, null=True, choices=STATES, verbose_name=_("State"))
    zip = models.CharField(max_length=10, blank=True, null=True, verbose_name=_("ZIP"))
    phone1 = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Phone 1"))
    phone2 = models.CharField(blank=True, null=True, max_length=20, verbose_name=_("Phone 2"))
    pws = models.ManyToManyField(PWS, blank=True, null=True, verbose_name=_("PWS"), related_name="employees")
    company = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Company"))
    has_licence_for_installation = models.BooleanField(default=False, verbose_name=_("Determines whether tester has access for installation"))

    def __unicode__(self):
        return str(self.user)

    def get_pws_list(self):
        return self.pws.all()

    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")
        permissions = (
            ('browse_user', _('Can browse Users')),
            ('access_to_adminpanel', _('Can log into Admin Panel')),
            ('access_to_all_users', _('Has access to all Users')),
            ('access_to_pws_users', _('Has access to PWS\'s Users')),
            ('access_to_multiple_pws_users', _('Has access to Users from multiple PWS')),
            ('access_to_audit_log', _('Has access to view PWS audit logs')),
        )

reversion.register(User, exclude=["last_login"])
reversion.register(Employee, follow=["user"])


class TestKit(models.Model):
    user = models.ForeignKey(User, verbose_name=_("Owner"), related_name='kits')
    test_serial = models.CharField(max_length=20, verbose_name=_("Test Serial"))
    test_manufacturer = models.ForeignKey(TestManufacturer, blank=True, null=True, verbose_name=_("Test Manufacturer"),
                                          related_name=_("kits"))
    test_model = models.ForeignKey(TestModel, blank=True, null=True, verbose_name=_("Test Model"),
                                   related_name=_("kits"))
    test_last_cert = models.DateField(blank=True, null=True, verbose_name=_("Last Cert."))
    is_active = models.BooleanField(default=True, verbose_name=_("Is still in use"))

    def __unicode__(self):
        return str(self.test_serial)

    def get_pws_list(self):
        return self.user.employee.pws.all()

    class Meta:
        verbose_name = _("Test Kit")
        verbose_name_plural = _("Test Kits")
        permissions = (
            ('access_to_all_test_kits', _("Access to all testers' kits")),
            ('access_to_pws_test_kits', _("Access to own PWS' testers' kits")),
        )

reversion.register(TestKit)


class TesterCert(models.Model):
    user = models.ForeignKey(User, verbose_name=_("Owner"), related_name='certs')
    cert_number = models.CharField(max_length=30, verbose_name=_("Cert. Number"))
    cert_date = models.DateField(blank=True, null=True, verbose_name=_("Cert. Date"))
    cert_expires = models.DateField(blank=True, null=True, verbose_name=_("Cert. Expires"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is still valid"))

    def __unicode__(self):
        return str(self.cert_number)

    def get_pws_list(self):
        return self.user.employee.pws.all()

    class Meta:
        verbose_name = _("Tester Certificate")
        verbose_name_plural = _("Tester Certificates")
        permissions = (
            ('access_to_all_tester_certs', _("Access to all testers' certs")),
            ('access_to_pws_tester_certs', _("Access to own PWS' testers' certs")),
        )

reversion.register(TesterCert)


class NoSearchFieldIndicated(Exception):
    pass


class Site(models.Model):
    pws = models.ForeignKey(PWS, verbose_name=_("PWS"), related_name="sites", db_index=True)
    connect_date = models.DateField(null=True, blank=True, verbose_name=_("Connect Date"))
    address1 = models.CharField(max_length=100, verbose_name=_("Service Street Address"))
    address2 = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Service Secondary Address"))
    street_number = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Service Street Number"))
    apt = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Service Apt"))
    city = models.CharField(max_length=30, verbose_name=_("Service City"))
    state = models.CharField(max_length=2, null=True, blank=True, choices=STATES, verbose_name=_("Service State"))
    zip = models.CharField(max_length=10, null=True, blank=True, verbose_name=_("Service ZIP"))
    site_use = models.ForeignKey(SiteUse, verbose_name=_("Site Use"), blank=True, null=True, related_name="sites")
    site_type = models.ForeignKey(SiteType, verbose_name=_("Site Type"), blank=True, null=True, related_name="sites")
    status = models.ForeignKey(SiteStatus, null=True, blank=True, verbose_name=_("Site Status"), related_name="sites")
    floors = models.ForeignKey(FloorsCount, verbose_name=_("Number of Floors"), blank=True, null=True, related_name="sites")
    interconnection_point = models.ForeignKey(ICPointType, verbose_name=_("Interconnection Point"), blank=True, null=True, related_name="sites")
    meter_number = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Meter Number"))
    meter_size = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Meter Size"))
    meter_reading = models.FloatField(blank=True, null=True, verbose_name=_("Meter Reading"))
    route = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Sequence Route"))
    potable_present = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Potable Present"))
    fire_present = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Fire Present"))
    irrigation_present = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Irrigation Present"))
    is_due_install = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Is Due Install"))
    is_backflow = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Is Backflow Present"))
    next_survey_date = models.DateField(null=True, blank=True, verbose_name=_("Next Survey Date"))
    notes = models.TextField(max_length=255, blank=True, null=True, verbose_name=_("Notes"))
    last_survey_date = models.DateField(null=True, blank=True, verbose_name=_("Last Survey Date"))
    cust_number = models.CharField(max_length=15, verbose_name=_("Account Number"), db_index=True)
    cust_name = models.CharField(max_length=50, verbose_name=_("Customer Name"))
    cust_code = models.ForeignKey(CustomerCode, verbose_name=_("Customer Code"), related_name="customers")
    cust_address1 = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Customer Main Address"))
    cust_address2 = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Customer Secondary Address"))
    cust_apt = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Customer Apt"))
    cust_city = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Customer City"))
    cust_state = models.CharField(max_length=2, null=True, blank=True, choices=STATES, verbose_name=_("Customer State"))
    cust_zip = models.CharField(null=True, blank=True, max_length=10, verbose_name=_("Customer ZIP"))
    contact_phone = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("Customer Phone"))
    contact_fax = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("Customer Fax"))
    contact_email = models.EmailField(max_length=30, blank=True, null=True, verbose_name=_("Customer Email"))
    due_install_test_date = models.DateField(blank=True, null=True, verbose_name=_("Due Test Date"))

    def __unicode__(self):
        return u"%s %s, %s %s" % (self.street_number or '', self.address1, self.city, self.zip or '')

    def get_pws_list(self):
        return [self.pws]

    def site_details_in_search_result(self):
        return u"{0} {1}, {2} {3} {4} {5}".format(
            self.street_number or '',
            self.address1 or '',
            self.city or '',
            self.zip or '',
            _("Customer number: ") + self.cust_number if self.cust_number else '',
            _("Meter number: ") + self.meter_number if self.meter_number else '')

    @staticmethod
    def search_in_cust_number_address_meter_number(pws, field, search_value):
        if field == 'cust_number':
            lookups = [models.Q(pws=pws, cust_number__iexact=search_value)]
        elif field == 'address':
            lookups = [models.Q(pws=pws, street_number__icontains=value) |
                       models.Q(pws=pws, address1__icontains=value) |
                       models.Q(pws=pws, address2__icontains=value)
                       for value in search_value.split()]
        elif field == 'meter_number':
            lookups = [models.Q(pws=pws, meter_number__iexact=search_value)]
        else:
            raise NoSearchFieldIndicated()
        return Site.objects.filter(*lookups)

    def get_absolute_url(self):
        return reverse('webapp:site_detail', args=(self.pk,))

    class Meta:
        verbose_name = _("Site")
        verbose_name_plural = _("Sites")
        unique_together = 'pws', 'cust_number'
        permissions = (
            ('browse_site', _('Can browse Site')),
            ('access_to_all_sites', _('Has access to all Sites')),
            ('access_to_pws_sites', _('Has access to PWS\'s Sites')),
            ('access_to_multiple_pws_sites', _('Has access to multiple PWS\' Sites')),
            ('access_to_site_by_customer_account', _('Has access to Site through Customer Account')),
            ('access_to_import', _('Can import Sites from Excel file')),
            ('access_to_batch_update', _('Has access to batch update')),
            ('change_all_info_about_site', _('Can change all information about Site')),
            ('export_xls', _('Can export sites into XLS file')),
        )

reversion.register(Site)


class BPDevice(models.Model):
    assembly_location = models.ForeignKey(AssemblyLocation, null=True, blank=True, verbose_name=_("Assembly Location"),
                                          related_name="hazards")
    installed_properly = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Installed Properly"))
    installer = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Installer"))
    install_date = models.DateField(blank=True, null=True, verbose_name=_("Install Date"))
    replace_date = models.DateField(null=True, blank=True, verbose_name=_("Replace Date"))
    orientation = models.ForeignKey(Orientation, null=True, blank=True, verbose_name=_('orientation'),
                                    related_name="hazards")
    bp_type_present = models.CharField(choices=BP_TYPE_CHOICES, max_length=15, verbose_name=_('BP Type Present'))
    bp_size = models.ForeignKey(BPSize, null=True, blank=True, verbose_name=_("BP Size"),
                                related_name="hazards")
    manufacturer = models.ForeignKey(BPManufacturer, null=True, blank=True, verbose_name=_("BP Manufacturer"),
                                     related_name="hazards")
    model_no = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("BP Model No."))
    serial_no = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("BP Serial No."))
    due_test_date = models.DateField(null=True, blank=True, verbose_name=_("Due Install/Test Date"))
    notes = models.TextField(max_length=255, blank=True, null=True, verbose_name=_("Notes"))

    def __unicode__(self):
        try:
            hazard = self.hazard
        except:
            hazard = 'Not installed'
        return u"%s, %s" % (self.bp_type_present, hazard)

    @property
    def paid_tests(self):
        return self.tests.filter(paid=True)

    class Meta:
        verbose_name = _("BP Device")
        verbose_name_plural = _("BP Devices")
        permissions = (
            ('browse_devices', _('Can browse BP Device')),
            ('access_to_all_devices', _('Has access to all BP Devices')),
            ('access_to_pws_devices', _('Has access to PWS\'s BP Devices')),
            ('access_to_multiple_pws_devices', _('Has access to multiple PWS\' BP Devices'))
        )

    def get_pws_list(self):
        try:
            return [self.hazard.site.pws]
        except:
            return []

reversion.register(BPDevice)


class Hazard(models.Model):
    site = models.ForeignKey(Site, verbose_name=_("Site"), related_name="hazards")
    location1 = models.CharField(max_length=70, blank=True, null=True, verbose_name=_("Location 1"))
    location2 = models.CharField(max_length=70, blank=True, null=True, verbose_name=_("Location 2"))
    latitude = models.FloatField(blank=True, null=True, verbose_name=_("Latitude"))
    longitude = models.FloatField(blank=True, null=True, verbose_name=_("Longitude"))
    regulation_type = models.ForeignKey(Regulation, verbose_name=_("Regulation"), null=True, blank=True,
                                        related_name="hazards")
    photo = models.ImageField(blank=True, null=True, default=None,
                              upload_to=photo_util.rename,
                              verbose_name=_('Photo'))
    photo_thumb = models.ImageField(blank=True, null=True, default=None, upload_to='photo/thumb/',
                                    verbose_name=_('Photo Thumbnail'))
    pump_present = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Pump Present"))
    additives_present = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Additives Present"))
    cc_present = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("CC Present"))
    aux_water = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Auxiliary Water"))
    service_type = models.ForeignKey(ServiceType, verbose_name=_("Service Type"), related_name="hazards")
    hazard_type = models.ForeignKey(HazardType, verbose_name=_("Hazard Type"), related_name="hazards")
    hazard_degree = models.ForeignKey(HazardDegree, null=True, blank=True, verbose_name=_("Hazard Degree"),
                                      related_name="hazards")
    assembly_status = models.CharField(choices=ASSEMBLY_STATUS_CHOICES, max_length=15, null=True, blank=True,
                                       verbose_name=_("Assembly Status"))
    bp_type_required = models.CharField(choices=BP_TYPE_CHOICES, max_length=15, null=True, blank=True,
                                        verbose_name=_('BP Type Required'))
    bp_device = models.OneToOneField(BPDevice, null=True, blank=True, related_name=_("hazard"))
    is_present = models.BooleanField(default=True, verbose_name=_("Is Present On Site"))
    notes = models.TextField(max_length=255, blank=True, null=True, verbose_name=_("Notes"))

    def __unicode__(self):
        return u"%s, %s, %s" % (self.hazard_type, self.service_type, self.site.cust_number)

    def get_pws_list(self):
        return [self.site.pws]

    class Meta:
        verbose_name = _("Hazard")
        verbose_name_plural = _("Hazards")
        permissions = (
            ('browse_hazard', _('Can browse Hazard')),
            ('access_to_all_hazards', _('Has access to all Hazards')),
            ('access_to_pws_hazards', _('Has access to PWS\'s Hazards')),
            ('access_to_multiple_pws_hazards', _('Has access to multiple PWS\' Hazards'))
        )

reversion.register(Hazard)


class Survey(models.Model):
    site = models.ForeignKey(Site, verbose_name=_("Site"), related_name="surveys")
    hazards = models.ManyToManyField(Hazard, verbose_name=_("Hazards"), related_name="surveys", blank=True, null=True)
    service_type = models.ForeignKey(ServiceType, verbose_name=_("Service Type"), related_name="surveys")
    survey_date = models.DateField(verbose_name=_("Survey Date"))
    survey_type = models.ForeignKey(SurveyType, blank=True, null=True, verbose_name=_("Survey Type"),
                                    related_name="surveys")
    surveyor = models.ForeignKey(User, null=True, blank=True, verbose_name=_("Surveyor"), related_name="surveys")
    metered = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Metered"))
    pump_present = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Pump Present"))
    additives_present = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Additives Present"))
    cc_present = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("CC Present"))
    protected = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Is Protected"))
    aux_water = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Auxiliary Water"))
    detector_manufacturer = models.CharField(max_length=20, blank=True, null=True,
                                             verbose_name=_("Detector Manufacturer"))
    detector_model = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Detector Model"))
    detector_serial_no = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Detector Serial No."))
    special = models.ForeignKey(Special, null=True, blank=True, verbose_name=_("Special"), related_name="surveys")
    notes = models.TextField(max_length=255, blank=True, null=True, verbose_name=_("Notes"))
    letter_type = models.ForeignKey(LetterType, blank=True, null=True, verbose_name=_("Letter Type"), related_name="survey_letter_types")

    def __unicode__(self):
        return u"%s, %s" % (self.survey_date, self.service_type)

    def get_pws_list(self):
        return [self.site.pws]

    class Meta:
        verbose_name = _("Survey")
        verbose_name_plural = _("Surveys")
        get_latest_by = 'survey_date'
        permissions = (
            ('browse_survey', _('Can browse Survey')),
            ('access_to_all_surveys', _('Has access to all Surveys')),
            ('access_to_pws_surveys', _('Has access to PWS\'s Surveys')),
            ('access_to_multiple_pws_surveys', _('Has access to multiple PWS\' Surveys')),
            ('access_to_own_surveys', _('Has access to own Surveys')),
        )
        ordering = ('-survey_date', '-id')

    def add_nhp_hazard(self):
        hazard_type = HazardType.objects.get(hazard_type=u'NHP')
        nhp_hazard = Hazard.objects.create(site=self.site, hazard_type=hazard_type, service_type=self.service_type)
        self.hazards.add(nhp_hazard)


reversion.register(Survey)


class Test(models.Model):
    bp_device = models.ForeignKey(BPDevice, verbose_name=_("BP Device"), related_name="tests")
    tester = models.ForeignKey(User, verbose_name=_("Tester"), related_name="tests")
    user = models.ForeignKey(User, verbose_name=_("Who added test into System"), related_name="added_tests")
    test_date = models.DateField(verbose_name=_("Test Date"), default=date.today)
    cv1_leaked = models.BooleanField(default=False, choices=VALVE_LEAKED_CHOICES, verbose_name=_("CV1 Leaked"))
    cv1_gauge_pressure = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True, verbose_name=_("CV1 Gauge Pressure"))
    cv1_retest_gauge_pressure = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True, verbose_name=_("CV1 Retest Gauge Pressure"))
    cv2_leaked = models.BooleanField(default=False, choices=VALVE_LEAKED_CHOICES, verbose_name=_("CV2 Leaked"))
    cv2_gauge_pressure = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True, verbose_name=_("CV2 Gauge Pressure"))
    cv2_retest_gauge_pressure = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True, verbose_name=_("CV2 Retest Gauge Pressure"))
    rv_opened = models.BooleanField(choices=VALVE_OPENED_CHOICES, default=False, verbose_name=_("RV Opened"))
    rv_psi1 = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True, verbose_name=_("RV Pressure 1"))
    rv_psi2 = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True, verbose_name=_("RV Pressure 2"))
    outlet_sov_leaked = models.BooleanField(choices=VALVE_LEAKED_CHOICES, default=False, verbose_name=_("Outlet SOV Leaked"))
    cv_leaked = models.BooleanField(choices=VALVE_LEAKED_CHOICES, default=False, verbose_name=_("CV Leaked"))
    cv_held_pressure = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True, verbose_name=_("CV Held Pressure"))
    air_inlet_opened = models.BooleanField(choices=YESNO_CHOICES, default=True, verbose_name=_("Air Inlet Opened"))
    air_inlet_psi = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True, verbose_name=_("Air Inlet PSI"))
    air_inlet_retest_psi = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True, verbose_name=_("Air Inlet Retest PSI"))
    cv_retest_psi = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True, verbose_name=_("CV Retest PSI"))
    test_result = models.BooleanField(choices=TEST_RESULT_CHOICES, default=False, verbose_name=_("Test Result"))
    notes = models.TextField(max_length=255, blank=True, null=True, verbose_name=_("Notes"))
    paid = models.BooleanField(default=False, verbose_name=_('Whether test paid?'))
    cv1_cleaned = models.CharField(choices=CLEANED_REPLACED_CHOICES, default=CLEANED_REPLACED_CHOICES[0][0],
                                   verbose_name=_("CV1 Cleaned or Replaced"), max_length=255)
    cv2_cleaned = models.CharField(choices=CLEANED_REPLACED_CHOICES, default=CLEANED_REPLACED_CHOICES[0][0],
                                   verbose_name=_("CV2 Cleaned or Replaced"), max_length=255)
    rv_cleaned = models.CharField(choices=CLEANED_REPLACED_CHOICES, default=CLEANED_REPLACED_CHOICES[0][0],
                                  verbose_name=_("RV Cleaned or Replaced"), max_length=255)
    pvb_cleaned = models.CharField(choices=CLEANED_REPLACED_CHOICES, default=CLEANED_REPLACED_CHOICES[0][0],
                                   verbose_name=_("PVB Cleaned or Replaced"), max_length=255)
    paypal_payment_id = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Paypal Payment ID'))
    cv1_detail_rubber_parts_kit = models.BooleanField(default=False, verbose_name=_('Rubber Parts Kit'))
    cv1_detail_cv_assembly = models.BooleanField(default=False, verbose_name=_('CV Assembly'))
    cv1_detail_disk = models.BooleanField(default=False, verbose_name=_('Disk'))
    cv1_detail_o_rings = models.BooleanField(default=False, verbose_name=_('O-Rings'))
    cv1_detail_seat = models.BooleanField(default=False, verbose_name=_('Seat'))
    cv1_detail_spring = models.BooleanField(default=False, verbose_name=_('Spring'))
    cv1_detail_stem_guide = models.BooleanField(default=False, verbose_name=_('Stem/Guide'))
    cv1_detail_retainer = models.BooleanField(default=False, verbose_name=_('Retainer'))
    cv1_detail_lock_nuts = models.BooleanField(default=False, verbose_name=_('Lock Nuts'))
    cv1_detail_other = models.BooleanField(default=False, verbose_name=_('Other'))
    rv_detail_rubber_parts_kit = models.BooleanField(default=False, verbose_name=_('Rubber Parts Kit'))
    rv_detail_rv_assembly = models.BooleanField(default=False, verbose_name=_('RV Assembly'))
    rv_detail_disk = models.BooleanField(default=False, verbose_name=_('Disk'))
    rv_detail_diaphragms = models.BooleanField(default=False, verbose_name=_('Diaphragm(s)'))
    rv_detail_seat = models.BooleanField(default=False, verbose_name=_('Seat'))
    rv_detail_spring = models.BooleanField(default=False, verbose_name=_('Spring'))
    rv_detail_guide = models.BooleanField(default=False, verbose_name=_('Guide'))
    rv_detail_o_rings = models.BooleanField(default=False, verbose_name=_('O-Rings'))
    rv_detail_other = models.BooleanField(default=False, verbose_name=_('Other'))
    cv2_detail_rubber_parts_kit = models.BooleanField(default=False, verbose_name=_('Rubber Parts Kit'))
    cv2_detail_cv_assembly = models.BooleanField(default=False, verbose_name=_('CV Assembly'))
    cv2_detail_disk = models.BooleanField(default=False, verbose_name=_('Disk'))
    cv2_detail_o_rings = models.BooleanField(default=False, verbose_name=_('O-Rings'))
    cv2_detail_seat = models.BooleanField(default=False, verbose_name=_('Seat'))
    cv2_detail_spring = models.BooleanField(default=False, verbose_name=_('Spring'))
    cv2_detail_stem_guide = models.BooleanField(default=False, verbose_name=_('Stem/Guide'))
    cv2_detail_retainer = models.BooleanField(default=False, verbose_name=_('Retainer'))
    cv2_detail_lock_nuts = models.BooleanField(default=False, verbose_name=_('Lock Nuts'))
    cv2_detail_other = models.BooleanField(default=False, verbose_name=_('Other'))
    pvb_detail_rubber_parts_kit = models.BooleanField(default=False, verbose_name=_('Rubber Parts Kit'))
    pvb_detail_rv_assembly = models.BooleanField(default=False, verbose_name=_('RV Assembly'))
    pvb_detail_disk_air_inlet = models.BooleanField(default=False, verbose_name=_('Disk, Air Inlet'))
    pvb_detail_disk_check_valve = models.BooleanField(default=False, verbose_name=_('Disk, Check Valve'))
    pvb_detail_seat_check_valve = models.BooleanField(default=False, verbose_name=_('Seat, Check Valve'))
    pvb_detail_spring_air_inlet = models.BooleanField(default=False, verbose_name=_('Spring, Air Inlet'))
    pvb_detail_spring_check_valve = models.BooleanField(default=False, verbose_name=_('Spring, Check Valve'))
    pvb_detail_guide = models.BooleanField(default=False, verbose_name=_('Guide'))
    pvb_detail_o_rings = models.BooleanField(default=False, verbose_name=_('O-Rings'))
    pvb_detail_other = models.BooleanField(default=False, verbose_name=_('Other'))
    test_kit = models.ForeignKey(TestKit, null=True, blank=True, verbose_name=_('Test Kit'), related_name='tests')
    tester_cert = models.ForeignKey(TesterCert, null=True, blank=True, verbose_name=_('Tester Cert'),
                                    related_name='tests')

    def __unicode__(self):
        return u"%s, %s" % (self.bp_device, self.test_date)

    def get_pws_list(self):
        return [self.bp_device.hazard.site.pws]

    @property
    def price(self):
        return self.bp_device.hazard.site.pws.price

    @property
    def cv1_replaced_details(self):
        return self._get_replaced_details('cv1')

    @property
    def rv_replaced_details(self):
        return self._get_replaced_details('rv')

    @property
    def cv2_replaced_details(self):
        return self._get_replaced_details('cv2')

    @property
    def pvb_replaced_details(self):
        return self._get_replaced_details('pvb')

    def _get_replaced_details(self, type):
        detail_fields = [field for field in self._meta.fields if field.name.startswith('%s_detail' % type)]
        details = [field.verbose_name for field in detail_fields if getattr(self, field.name) is True]
        return details

    class Meta:
        verbose_name = _("Test")
        verbose_name_plural = _("Tests")
        permissions = (
            ('browse_test', _('Can browse Test')),
            ('access_to_all_tests', _('Has access to all Tests')),
            ('access_to_pws_tests', _('Has access to PWS\'s Tests')),
            ('access_to_multiple_pws_tests', _('Has access to multiple PWS\' Tests')),
            ('access_to_own_tests', _('Has access to own Tests')),
        )
        ordering = ('-test_date', '-id')

reversion.register(Test)


class Letter(models.Model):
    site = models.ForeignKey(Site, blank=True, null=True, verbose_name=_("Site"), related_name="letters")
    hazard = models.ForeignKey(Hazard, blank=True, null=True, verbose_name=_("Hazard"), related_name="letters")
    letter_type = models.ForeignKey(LetterType, verbose_name=_("Letter Type"), related_name="letters")
    date = models.DateField(verbose_name=_("Send Date"), auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank=True, verbose_name=_("Sender"), related_name="letters")
    already_sent = models.BooleanField(default=False, verbose_name="Already Sent")
    rendered_body = models.TextField(null=True, blank=True, verbose_name=_("Letter Content"))

    def __unicode__(self):
        return u"%s, %s" % (self.date, self.letter_type)

    def get_pws_list(self):
        return [self.site.pws]

    class Meta:
        verbose_name = _("Letter")
        verbose_name_plural = _("Letters")
        permissions = (
            ('browse_letter', _('Can browse Letter')),
            ('send_letter', _('Can send Letter')),
            ('pws_letter_access', _('Has access to pws letters')),
            ('multiple_pws_letter_access', _('Has access to multiple pws\' letters')),
            ('full_letter_access', _('Has access to all letters'))
        )

reversion.register(Letter)


class StaticText(models.Model):
    title = models.CharField(max_length=20, verbose_name=_('Title'))
    group = models.ForeignKey(Group, blank=True, null=True, verbose_name=_('Group'), related_name="static_texts")
    text = RichTextField(null=True, blank=True, verbose_name=_('Text'))

    def __unicode__(self):
        return u"%s" % self.title

    class Meta:
        verbose_name = _("Static Text")
        verbose_name_plural = _("Static Texts")

reversion.register(StaticText)


class ImportLog(models.Model):
    user = models.ForeignKey(User, related_name='import_logs', verbose_name=_('User who performed import'))
    pws = models.ForeignKey(PWS, related_name='import_logs', verbose_name=_('PWS for which import was performed'))
    datetime = models.DateTimeField(auto_now_add=True, verbose_name=_('Datetime of import'))
    added_sites = models.ManyToManyField(Site, related_name='added_imports', verbose_name=_('Added sites'))
    updated_sites = models.ManyToManyField(Site, related_name='updated_imports', verbose_name=_('Updated sites'))
    deactivated_sites = models.ManyToManyField(Site, related_name='deactivated_imports', verbose_name=_('Deactivated sites'))
    progress = models.IntegerField(default=0, verbose_name=_('Progress of import'))

    def get_pws_list(self):
        return [self.pws]

    class Meta:
        verbose_name = _('Import Log')
        verbose_name_plural = _('Import Logs')
        permissions = (
            ('browse_import_log', _('Can browse Import Log')),
            ('access_to_all_import_logs', _('Has access to all Import Logs')),
            ('access_to_pws_import_logs', _('Has access to PWS\'s Import Logs')),
        )

reversion.register(ImportLog)


class Invite(models.Model):
    invite_date = models.DateField(auto_now_add=True, verbose_name=_('Invite sending date'))
    invite_from = models.ForeignKey(User, verbose_name=_('Invite sender'), related_name='invites_sent')
    invite_to = models.ForeignKey(User, verbose_name=_('Invited tester'), related_name='invites_received')
    invite_pws = models.ManyToManyField(PWS, verbose_name=_('Invite to PWS'))
    accepted = models.BooleanField(default=False)
    code = models.CharField(max_length=64, default=uuid.uuid4)

    def get_pws_list(self):
        return self.invite_pws.all()

    class Meta:
        verbose_name = _('Invite')
        verbose_name_plural = _('Invites')

reversion.register(Invite)

import signals