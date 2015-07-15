from decimal import Decimal
from datetime import date

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User, Group
from ckeditor.fields import RichTextField

from main.parameters import *
from utils import photo_util
import fields


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


class AssemblyStatus(models.Model):
    assembly_status = models.CharField(max_length=20, verbose_name=_("Assembly Status"))

    def __unicode__(self):
        return u"%s" % self.assembly_status

    class Meta:
        verbose_name = _('Assembly Status')
        verbose_name_plural = _('Assembly Statuses')
        ordering = ('assembly_status',)
        permissions = (
            ('browse_assemblystatus', _('Can browse Assembly Status')),
        )


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

    class Meta:
        verbose_name = _('Public Water System')
        verbose_name_plural = _('Public Water Systems')
        ordering = ('number',)
        permissions = (
            ('browse_pws', _('Can browse Public Water System')),
            ('browse_all_pws', _('Can browse all Public Water Systems')),
            ('change_own_pws', _('Can change his own Public Water System'))
        )


class LetterType(models.Model):
    letter_type = models.CharField(max_length=20, verbose_name=_("Letter Type"))
    template = RichTextField(blank=False, null=False, default=_('Default Letter Template'), verbose_name=_('Letter Template'))
    header = models.CharField(blank=False, null=False, default=_('Backflow Prevention Services Notification'), verbose_name=_('Letter Header'), max_length=150)
    pws = models.ForeignKey(PWS, null=True, blank=True, default=None, related_name='letter_types')

    def __unicode__(self):
        return u"%s" % self.letter_type

    class Meta:
        verbose_name = _('Letter Type')
        verbose_name_plural = _('Letter Types')
        unique_together = 'letter_type', 'pws'
        ordering = ('letter_type',)
        permissions = (
            ('browse_lettertype', _('Can browse Letter Type')),
            ('access_to_all_lettertypes', _('Has access to all Letter Types')),
            ('access_to_pws_lettertypes', _('Has access to PWS\'s Letter Types')),
        )


class Employee(models.Model):
    user = models.OneToOneField(User)
    address = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Address"))
    city = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("City"))
    state = models.CharField(max_length=2, blank=True, null=True, choices=STATES, verbose_name=_("State"))
    zip = models.CharField(max_length=10, blank=True, null=True, verbose_name=_("ZIP"))
    phone1 = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Phone 1"))
    phone2 = models.CharField(blank=True, null=True, max_length=20, verbose_name=_("Phone 2"))
    pws = models.ForeignKey(PWS, blank=True, null=True, verbose_name=_("PWS"), related_name="employees")
    cert_number = models.CharField(blank=True, null=True, max_length=30, verbose_name=_("Cert. Number"))
    cert_date = models.DateField(blank=True, null=True, verbose_name=_("Cert. Date"))
    cert_expires = models.DateField(blank=True, null=True, verbose_name=_("Cert. Expires"))
    test_manufacturer = models.ForeignKey(TestManufacturer, blank=True, null=True, verbose_name=_("Test Manufacturer"),
                                          related_name=_("testers"))
    test_model = models.ForeignKey(TestModel, blank=True, null=True, verbose_name=_("Test Model"),
                                   related_name=_("testers"))
    test_last_cert = models.DateField(blank=True, null=True, verbose_name=_("Last Cert."))
    company = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Company"))
    test_serial = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Test Serial"))
    has_licence_for_installation = models.BooleanField(default=False, verbose_name=_("Determines whether tester has access for installation"))

    def __unicode__(self):
        return str(self.user)

    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")
        permissions = (
            ('browse_user', _('Can browse Users')),
            ('access_to_adminpanel', _('Can log into Admin Panel')),
            ('access_to_all_users', _('Has access to all Users')),
            ('access_to_pws_users', _('Has access to PWS\'s Users')),
        )


class Site(models.Model):
    pws = models.ForeignKey(PWS, verbose_name=_("PWS"), related_name="sites", help_text=_("PWS which Site belongs"), db_index=True)
    connect_date = models.DateField(null=True, blank=True, verbose_name=_("Connect Date"), help_text=_("Connection date of Site"))
    address1 = models.CharField(max_length=100, verbose_name=_("Address 1"), help_text=_("Main Address of Site"))
    address2 = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Address 2"), help_text=_("Secondary Address of Site if exists"))
    street_number = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Street Number'), help_text=_("Site Address's Street Number"))
    apt = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("Apt"), help_text=_("Site Address's Apartment"))
    city = models.CharField(max_length=30, verbose_name=_("City"), help_text=_("Site's City"))
    state = models.CharField(max_length=2, null=True, blank=True, choices=STATES, verbose_name=_("State"), help_text=_("Site's State"))
    zip = models.CharField(max_length=10, null=True, blank=True, verbose_name=_("ZIP"), help_text=_("Site's ZIP Code"))
    site_use = models.ForeignKey(SiteUse, verbose_name=_("Site Use"), blank=True, null=True, related_name="sites", help_text=_("Using of Site"))
    site_type = models.ForeignKey(SiteType, verbose_name=_("Site Type"), blank=True, null=True, related_name="sites", help_text=_("Type of Site"))
    status = models.ForeignKey(SiteStatus, null=True, blank=True, verbose_name=_("Status"), related_name="sites", help_text=_("Site's Status"))
    floors = models.ForeignKey(FloorsCount, verbose_name=_("Building Height"), blank=True, null=True,
                               related_name="sites", help_text=_("Number of Floors"))
    interconnection_point = models.ForeignKey(ICPointType, verbose_name=_("Interconnection Point"), blank=True,
                                              null=True, related_name="sites", help_text=_("Interconnection Point Type"))
    meter_number = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Meter Number"), help_text=_("Meter Number"))
    meter_size = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("Meter Size"), help_text=_("Meter Size"))
    meter_reading = models.FloatField(blank=True, null=True, verbose_name=_("Meter Reading"), help_text=_("Meter Reading"))
    route = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Seq. Route"), help_text=_("Sequence Route"))
    potable_present = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Potable Present"), help_text=_("Is Potable connection present"))
    fire_present = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Fire Present"), help_text=_("Is Fire connection present"))
    irrigation_present = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Irrigation Present"), help_text=_("Is Irrigation connection present"))
    is_due_install = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Is Due Install"), help_text=_("Is Due Install"))
    is_backflow = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Is Backflow Present"), help_text=_("Is Backflow present"))
    next_survey_date = models.DateField(null=True, blank=True, verbose_name=_("Next Survey Date"), help_text=_("Next Survey Date"))
    notes = models.TextField(max_length=255, blank=True, null=True, verbose_name=_("Notes"), help_text=_("Notes"))
    last_survey_date = models.DateField(null=True, blank=True, verbose_name=_("Last Survey Date"), help_text=_("Last Survey Date"))
    cust_number = models.CharField(max_length=15, verbose_name=_("Number"), help_text=_("Customer's Number"), db_index=True)
    cust_name = models.CharField(max_length=50, verbose_name=_("Name"), help_text=_("Customer's Name"))
    cust_code = models.ForeignKey(CustomerCode, verbose_name=_("Customer Code"), related_name="customers", help_text=_("Customer's Code"))
    cust_address1 = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Address 1"), help_text=_("Customer's Main Address"))
    cust_address2 = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Address 2"), help_text=_("Customer's Secondary Address (if exists)"))
    cust_apt = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("Customer Apt"), help_text=_("Customer's Apartment"))
    cust_city = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("City"), help_text=_("Customer's City"))
    cust_state = models.CharField(max_length=2, null=True, blank=True, choices=STATES, verbose_name=_("State"), help_text=_("Customer's State"))
    cust_zip = models.CharField(null=True, blank=True, max_length=10, verbose_name=_("ZIP"), help_text=_("Customer's ZIP Code"))
    contact_phone = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("Phone"), help_text=_("Customer's Phone"))
    contact_fax = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("Fax"), help_text=_("Customer's Fax"))
    contact_email = models.EmailField(max_length=30, blank=True, null=True, verbose_name=_("Email"), help_text=_("Customer's Email Address"))

    def __unicode__(self):
        return u"%s %s, %s %s" % (self.street_number or '', self.address1, self.city, self.zip or '')

    class Meta:
        verbose_name = _("Site")
        verbose_name_plural = _("Sites")
        unique_together = 'pws', 'cust_number'
        permissions = (
            ('browse_site', _('Can browse Site')),
            ('access_to_all_sites', _('Has access to all Sites')),
            ('access_to_pws_sites', _('Has access to PWS\'s Sites')),
            ('access_to_site_by_customer_account', _('Has access to Site through Customer Account')),
            ('access_to_import', _('Can import Sites from Excel file')),
            ('access_to_batch_update', _('Has access to batch update')),
            ('change_all_info_about_site', _('Can change all information about Site')),
        )


class Hazard(models.Model):
    site = models.ForeignKey(Site, verbose_name=_("Site"), related_name="hazards")
    location1 = models.CharField(max_length=70, blank=True, null=True, verbose_name=_("Location 1"))
    location2 = models.CharField(max_length=70, blank=True, null=True, verbose_name=_("Location 2"))
    latitude = models.FloatField(blank=True, null=True, verbose_name=_("Latitude"))
    longitude = models.FloatField(blank=True, null=True, verbose_name=_("Longitude"))
    regulation_type = models.ForeignKey(Regulation, verbose_name=_("Regulation"), null=True, blank=True, related_name="hazards")
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
    assembly_location = models.ForeignKey(AssemblyLocation, null=True, blank=True, verbose_name=_("Assembly Location"),
                                          related_name="hazards")
    assembly_status = models.ForeignKey(AssemblyStatus, null=True, blank=True, verbose_name=_("Assembly Status"),
                                        related_name="hazards")
    installed_properly = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Installed Properly"))
    installer = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Installer"))
    install_date = models.DateField(blank=True, null=True, verbose_name=_("Install Date"))
    replace_date = models.DateField(null=True, blank=True, verbose_name=_("Replace Date"))
    orientation = models.ForeignKey(Orientation, null=True, blank=True, verbose_name=_('orientation'),
                                    related_name="hazards")
    bp_type_present = models.CharField(choices=BP_TYPE_CHOICES, max_length=15, null=True, blank=True, verbose_name=_('BP Type Present'))
    bp_type_required = models.CharField(choices=BP_TYPE_CHOICES, max_length=15, null=True, blank=True, verbose_name=_('BP Type Required'))
    bp_size = models.ForeignKey(BPSize, null=True, blank=True, verbose_name=_("BP Size"),
                                related_name="hazards")
    manufacturer = models.ForeignKey(BPManufacturer, null=True, blank=True, verbose_name=_("BP Manufacturer"),
                                     related_name="hazards")
    model_no = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("BP Model No."))
    serial_no = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("BP Serial No."))
    due_install_test_date = models.DateField(null=True, blank=True, verbose_name=_("Due Install/Test Date"))
    is_present = models.BooleanField(default=True, verbose_name=_("Is Present On Site"))
    notes = models.TextField(max_length=255, blank=True, null=True, verbose_name=_("Notes"))

    def __unicode__(self):
        return u"%s, %s" % (self.hazard_type, self.service_type)

    @property
    def paid_tests(self):
        return self.tests.filter(paid=True)

    class Meta:
        verbose_name = _("Hazard")
        verbose_name_plural = _("Hazards")
        permissions = (
            ('browse_hazard', _('Can browse Hazard')),
            ('access_to_all_hazards', _('Has access to all Hazards')),
            ('access_to_pws_hazards', _('Has access to PWS\'s Hazards')),
            ('change_all_info_about_hazard', _('Can change all information about Hazard')),
        )


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

    def __unicode__(self):
        return u"%s, %s" % (self.survey_date, self.service_type)

    class Meta:
        verbose_name = _("Survey")
        verbose_name_plural = _("Surveys")
        get_latest_by = 'survey_date'
        permissions = (
            ('browse_survey', _('Can browse Survey')),
            ('access_to_all_surveys', _('Has access to all Surveys')),
            ('access_to_pws_surveys', _('Has access to PWS\'s Surveys')),
            ('access_to_own_surveys', _('Has access to own Surveys')),
        )
        ordering = ('-survey_date', '-id')


class Detail(models.Model):
    detail = models.CharField(max_length=100, verbose_name=_('Detail'))

    def __unicode__(self):
        return u'%s' % self.detail


class Test(models.Model):
    bp_device = models.ForeignKey(Hazard, verbose_name=_("BP Device"),
                                  related_name="tests")
    tester = models.ForeignKey(User, verbose_name=_("Tester"), related_name="tests")
    user = models.ForeignKey(User, verbose_name=_("Who added test into System"), related_name="added_tests")
    test_date = models.DateField(verbose_name=_("Test Date"), default=date.today)
    cv1_leaked = models.BooleanField(default=False, choices=VALVE_LEAKED_CHOICES, verbose_name=_("CV1 Leaked"))
    cv1_gauge_pressure = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True, verbose_name=_("CV1 Gauge Pressure"))
    cv1_maintenance = models.BooleanField(default=False, choices=YESNO_CHOICES, verbose_name=_("CV1 Maintenance"))
    cv1_maintenance_pressure = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True, verbose_name=_("CV1 Maintenance Pressure"))
    cv2_leaked = models.BooleanField(default=False, choices=VALVE_LEAKED_CHOICES, verbose_name=_("CV2 Leaked"))
    cv2_gauge_pressure = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True, verbose_name=_("CV2 Gauge Pressure"))
    cv2_maintenance = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("CV2 Maintenance"))
    cv2_maintenance_pressure = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True, verbose_name=_("CV2 Maintenance Pressure"))
    rv_opened = models.BooleanField(choices=VALVE_OPENED_CHOICES, default=False, verbose_name=_("RV Opened"))
    rv_psi1 = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True, verbose_name=_("RV Pressure 1"))
    rv_psi2 = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True, verbose_name=_("RV Pressure 2"))
    rv_maintenance = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("RV Maintenance"))
    outlet_sov_leaked = models.BooleanField(choices=VALVE_LEAKED_CHOICES, default=False,
                                            verbose_name=_("Outlet SOV Leaked"))
    pvb_opened = models.BooleanField(choices=VALVE_OPENED_CHOICES, default=False, verbose_name=_("PVB Opened"))
    pvb_open_pressure = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True, verbose_name=_("PVB Open Pressure"))
    cv_leaked = models.BooleanField(choices=VALVE_LEAKED_CHOICES, default=False, verbose_name=_("CV Leaked"))
    cv_held_pressure = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True, verbose_name=_("CV Held Pressure"))
    cv_maintenance = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("CV Maintenance"))
    air_inlet_opened = models.BooleanField(choices=YESNO_CHOICES, default=True, verbose_name=_("Air Inlet Opened"))
    air_inlet_psi = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True, verbose_name=_("Air Inlet PSI"))
    air_inlet_retest_psi = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True, verbose_name=_("Air Inlet Retest PSI"))
    cv_psi = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True, verbose_name=_("CV PSI"))
    cv_retest_psi = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True, verbose_name=_("CV Retest PSI"))
    test_result = models.BooleanField(choices=TEST_RESULT_CHOICES, default=False, verbose_name=_("Test Result"))
    notes = models.TextField(max_length=255, blank=True, null=True, verbose_name=_("Notes"))
    cv1_cleaned = models.BooleanField(choices=CLEANED_REPLACED_CHOICES, default=True, verbose_name=_("CV1 Cleaned or Replaced"))
    cv2_cleaned = models.BooleanField(choices=CLEANED_REPLACED_CHOICES, default=True, verbose_name=_("CV2 Cleaned or Replaced"))
    rv_cleaned = models.BooleanField(choices=CLEANED_REPLACED_CHOICES, default=True, verbose_name=_("RV Cleaned or Replaced"))
    pvb_cleaned = models.BooleanField(choices=CLEANED_REPLACED_CHOICES, default=True, verbose_name=_("PVB Cleaned or Replaced"))
    cv1_replaced_details = models.ManyToManyField(Detail, null=True, blank=True, related_name='cv1_replacements')
    cv2_replaced_details = models.ManyToManyField(Detail, null=True, blank=True, related_name='cv2_replacements')
    rv_replaced_details = models.ManyToManyField(Detail, null=True, blank=True, related_name='rv_replacements')
    pvb_replaced_details = models.ManyToManyField(Detail, null=True, blank=True, related_name='pvb_replacements')
    paid = models.BooleanField(default=False, verbose_name=_('Was test paid?'))
    paypal_payment_id = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Paypal Payment ID'))

    def __unicode__(self):
        return u"%s, %s" % (self.bp_device, self.test_date)

    @property
    def price(self):
        return self.bp_device.site.pws.price

    class Meta:
        verbose_name = _("Test")
        verbose_name_plural = _("Tests")
        permissions = (
            ('browse_test', _('Can browse Test')),
            ('access_to_all_tests', _('Has access to all Tests')),
            ('access_to_pws_tests', _('Has access to PWS\'s Tests')),
            ('access_to_own_tests', _('Has access to own Tests')),
        )
        ordering = ('-test_date', '-id')


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

    class Meta:
        verbose_name = _("Letter")
        verbose_name_plural = _("Letters")
        permissions = (
            ('browse_letter', _('Can browse Letter')),
            ('send_letter', _('Can send Letter')),
            ('pws_letter_access', _('Has access to pws letters')),
            ('full_letter_access', _('Has access to all letters'))
        )


class Licence(models.Model):
    given_to = models.ForeignKey(User, verbose_name=_("Given To"), related_name="licences")
    given_by = models.ForeignKey(User, null=True, blank=True, verbose_name=_("Given By"), related_name="licences_given")
    start_date = models.DateField(verbose_name=_("Start Date"))
    end_date = models.DateField(verbose_name=_("End Date"))
    is_active = models.BooleanField(verbose_name=_("Is Active"), default=True)
    notes = models.TextField(max_length=255, blank=True, null=True, verbose_name=_("Notes"))

    def __unicode__(self):
        return u"%s %s, %s" % (self.given_to.first_name, self.given_to.last_name, self.start_date)

    class Meta:
        verbose_name = "Licence"
        verbose_name_plural = "Licences"
        permissions = (
            ('browse_licence', _('Can browse Licence')),
        )


class StaticText(models.Model):
    title = models.CharField(max_length=20, verbose_name=_('Title'))
    group = models.ForeignKey(Group, blank=True, null=True, verbose_name=_('Group'), related_name="static_texts")
    text = RichTextField(null=True, blank=True, verbose_name=_('Text'))

    def __unicode__(self):
        return u"%s" % self.title

    class Meta:
        verbose_name = _("Static Text")
        verbose_name_plural = _("Static Text")


class ImportLog(models.Model):
    user = models.ForeignKey(User)
    pws = models.ForeignKey(PWS)
    datetime = models.DateTimeField(auto_now_add=True)
    added_sites = models.ManyToManyField(Site, related_name='added_imports')
    updated_sites = models.ManyToManyField(Site, related_name='updated_imports')
    deactivated_sites = models.ManyToManyField(Site, related_name='deactivated_imports')
    progress = models.IntegerField(default=0)

    class Meta:
        permissions = (
            ('browse_import_log', _('Can browse Import Log')),
            ('access_to_all_import_logs', _('Has access to all Import Logs')),
            ('access_to_pws_import_logs', _('Has access to PWS\'s Import Logs')),
        )


import signals