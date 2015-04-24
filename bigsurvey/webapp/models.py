from django.db import models
from django.utils.translation import ugettext as _
from main.parameters import *
from django.contrib.auth.models import User, Group


class SourceType(models.Model):
    source_type = models.CharField(max_length=50, verbose_name=_("Source Type"))

    def __unicode__(self):
        return u"%s" % self.source_type

    class Meta:
        verbose_name = _('Source Type')
        verbose_name_plural = _('Source Types')
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
        permissions = (
            ('browse_surveytype', _('Can browse Survey Type')),
        )


class BPType(models.Model):
    bp_type = models.CharField(max_length=10, verbose_name=_("BFP Type"))

    def __unicode__(self):
        return u"%s" % self.bp_type

    class Meta:
        verbose_name = _('BFP Type')
        verbose_name_plural = _('BFP Types')
        permissions = (
            ('browse_bptype', _('Can browse BP Type')),
        )


class BPSize(models.Model):
    bp_size = models.CharField(max_length=10, verbose_name=_("BFP Size"))

    def __unicode__(self):
        return u"%s" % self.bp_size

    class Meta:
        verbose_name = _('BFP Size')
        verbose_name_plural = _('BFP Sizes')
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
        permissions = (
            ('browse_assemblystatus', _('Can browse Assembly Status')),
        )


class LetterType(models.Model):
    letter_type = models.CharField(max_length=20, verbose_name=_("Letter Type"))
    template = models.TextField(max_length=2000, blank=True, null=True, verbose_name=_('Letter Template'))

    def __unicode__(self):
        return u"%s" % self.letter_type

    class Meta:
        verbose_name = _('Letter Type')
        verbose_name_plural = _('Letter Types')
        permissions = (
            ('browse_lettertype', _('Can browse Letter Type')),
        )


class FloorsCount(models.Model):
    floors_count = models.CharField(max_length=10, verbose_name=_("Floors Count"))

    def __unicode__(self):
        return u"%s" % self.floors_count

    class Meta:
        verbose_name = _('Floors Count')
        verbose_name_plural = _('Floors Count')
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
        permissions = (
            ('browse_sitestatus', _('Can browse Site Status')),
        )


class Customer(models.Model):
    number = models.CharField(max_length=15, unique=True, verbose_name=_("Number"))
    name = models.CharField(max_length=50, verbose_name=_("Name"))
    code = models.ForeignKey(CustomerCode, verbose_name=_("Customer Code"), related_name="customers")
    address1 = models.CharField(max_length=100, verbose_name=_("Address 1"))
    address2 = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Address 2"))
    apt = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("Customer Apt"))
    city = models.CharField(max_length=30, verbose_name=_("City"))
    state = models.CharField(max_length=2, null=True, blank=True, choices=STATES, verbose_name=_("State"))
    zip = models.CharField(null=True, blank=True, max_length=10, verbose_name=_("ZIP"))
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("Phone"))
    fax = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("Fax"))
    email = models.EmailField(max_length=15, blank=True, null=True, verbose_name=_("Email"))
    notes = models.TextField(max_length=255, blank=True, null=True, verbose_name=_("Notes"))

    def __unicode__(self):
        return u"%s, %s" % (self.name, self.city)

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
        permissions = (
            ('browse_customer', _('Can browse Customer')),
        )


class PWS(models.Model):
    number = models.CharField(max_length=15, verbose_name=_("Number"))
    name = models.CharField(max_length=50, verbose_name=_("Name"))
    city = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("City"))
    office_address = models.CharField(blank=True, null=True, max_length=50, verbose_name=_("Office Address"))
    water_source = models.ForeignKey(SourceType, blank=True, null=True, verbose_name=_("Water Source"),
                                     related_name="pws")
    notes = models.TextField(max_length=255, blank=True, null=True, verbose_name=_("Notes"))

    def __unicode__(self):
        return u"%s, %s" % (self.number, self.name)

    class Meta:
        verbose_name = _('Public Water System')
        verbose_name_plural = _('Public Water Systems')
        permissions = (
            ('browse_pws', _('Can browse Public Water System')),
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
    status = models.ForeignKey(SiteStatus, null=True, blank=True, verbose_name=_("Status"), related_name="sites")
    customer = models.ForeignKey(Customer, verbose_name=_("Customer"), related_name="sites")
    pws = models.ForeignKey(PWS, verbose_name=_("PWS"), related_name="sites")
    connect_date = models.DateField(null=True, blank=True, verbose_name=_("Connect Date"))
    address1 = models.CharField(max_length=100, verbose_name=_("Address 1"))
    address2 = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Address 2"))
    street_number = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Street Number'))
    apt = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("Apt"))
    city = models.CharField(max_length=30, verbose_name=_("City"))
    state = models.CharField(max_length=2, null=True, blank=True, choices=STATES, verbose_name=_("State"))
    zip = models.CharField(max_length=10, null=True, blank=True, verbose_name=_("ZIP"))
    site_use = models.ForeignKey(SiteUse, verbose_name=_("Site Use"), blank=True, null=True, related_name="sites")
    site_type = models.ForeignKey(SiteType, verbose_name=_("Site Type"), blank=True, null=True, related_name="sites")
    floors = models.ForeignKey(FloorsCount, verbose_name=_("Building Height"), blank=True, null=True,
                               related_name="sites")
    interconnection_point = models.ForeignKey(ICPointType, verbose_name=_("Interconnection Point"), blank=True,
                                              null=True, related_name="sites")
    meter_number = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Meter Number"))
    meter_size = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("Meter Size"))
    meter_reading = models.FloatField(blank=True, null=True, verbose_name=_("Meter Reading"))
    route = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Seq. Route"))
    potable_present = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Potable Present"))
    fire_present = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Fire Present"))
    irrigation_present = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Irrigation Present"))
    is_due_install = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Is Due Install"))
    is_backflow = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Is Backflow Present"))
    next_survey_date = models.DateField(null=True, blank=True, verbose_name=_("Next Survey Date"))
    notes = models.TextField(max_length=255, blank=True, null=True, verbose_name=_("Notes"))
    last_survey_date = models.DateField(null=True, blank=True, verbose_name=_("Last survey date"))

    def __unicode__(self):
        return u"%s, %s" % (self.city, self.address1)

    class Meta:
        verbose_name = _("Site")
        verbose_name_plural = _("Sites")
        permissions = (
            ('browse_site', _('Can browse Site')),
            ('access_to_all_sites', _('Has access to all Sites')),
            ('access_to_pws_sites', _('Has access to PWS\'s Sites')),
            ('access_to_import', _('Can import Sites from Excel file')),
            ('access_to_batch_update', _('Has access to batch update')),
            ('change_all_info_about_site', _('Can change all information about Site')),
        )


class Hazard(models.Model):
    site = models.ForeignKey(Site, verbose_name=_("Site"), related_name="hazards")
    location1 = models.CharField(max_length=70, blank=True, null=True, verbose_name=_("Location 1"))
    location2 = models.CharField(max_length=70, blank=True, null=True, verbose_name=_("Location 2"))
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
    bp_type_present = models.ForeignKey(BPType, null=True, blank=True, verbose_name=_('BP Type Present'),
                                        related_name='hazards_p')
    bp_type_required = models.ForeignKey(BPType, null=True, blank=True, verbose_name=_('BP Type Required'),
                                         related_name='hazards_r')
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
        return u"%s, %s" % (self.hazard_type, self.location1)

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


class Test(models.Model):
    bp_device = models.ForeignKey(Hazard, verbose_name=_("BP Device"),
                                  related_name="tests")
    tester = models.ForeignKey(User, verbose_name=_("Tester"), related_name="tests")
    test_date = models.DateField(verbose_name=_("Test Date"), auto_now_add=True)
    cv1_leaked = models.BooleanField(default=False, choices=VALVE_LEAKED_CHOICES, verbose_name=_("CV1 Leaked"))
    cv1_gauge_pressure = models.FloatField(blank=True, null=True, verbose_name=_("CV1 Gauge Pressure"))
    cv1_maintenance = models.BooleanField(default=False, choices=YESNO_CHOICES, verbose_name=_("CV1 Maintenance"))
    cv1_maintenance_pressure = models.FloatField(blank=True, null=True, verbose_name=_("CV1 Maintenance Pressure"))
    cv2_leaked = models.BooleanField(default=False, choices=VALVE_LEAKED_CHOICES, verbose_name=_("CV2 Leaked"))
    cv2_gauge_pressure = models.FloatField(blank=True, null=True, verbose_name=_("CV2 Gauge Pressure"))
    cv2_maintenance = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("CV2 Maintenance"))
    cv2_maintenance_pressure = models.FloatField(null=True, blank=True, verbose_name=_("CV2 Maintenance Pressure"))
    rv_opened = models.BooleanField(choices=VALVE_OPENED_CHOICES, default=False, verbose_name=_("RV Opened"))
    rv_psi1 = models.FloatField(null=True, blank=True, verbose_name=_("RV Pressure 1"))
    rv_psi2 = models.FloatField(null=True, blank=True, verbose_name=_("RV Pressure 2"))
    rv_maintenance = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("RV Maintenance"))
    outlet_sov_leaked = models.BooleanField(choices=VALVE_LEAKED_CHOICES, default=False,
                                            verbose_name=_("Outlet SOV Leaked"))
    pvb_opened = models.BooleanField(choices=VALVE_OPENED_CHOICES, default=False, verbose_name=_("PVB Opened"))
    pvb_open_pressure = models.FloatField(null=True, blank=True, verbose_name=_("PVB Open Pressure"))
    cv_leaked = models.BooleanField(choices=VALVE_LEAKED_CHOICES, default=False, verbose_name=_("CV Leaked"))
    cv_held_pressure = models.FloatField(null=True, blank=True, verbose_name=_("CV Held Pressure"))
    cv_maintenance = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("CV Maintenance"))
    air_inlet_opened = models.BooleanField(choices=YESNO_CHOICES, default=True, verbose_name=_("Air Inlet Opened"))
    air_inlet_psi = models.FloatField(null=True, blank=True, verbose_name=_("Air Inlet PSI"))
    cv_psi = models.FloatField(null=True, blank=True, verbose_name=_("CV PSI"))
    test_result = models.BooleanField(choices=TEST_RESULT_CHOICES, default=False, verbose_name=_("Test Result"))
    notes = models.TextField(max_length=255, blank=True, null=True, verbose_name=_("Notes"))

    def __unicode__(self):
        return u"%s, %s" % (self.bp_device, self.test_date)

    class Meta:
        verbose_name = _("Test")
        verbose_name_plural = _("Tests")
        permissions = (
            ('browse_test', _('Can browse Test')),
            ('access_to_all_tests', _('Has access to all Tests')),
            ('access_to_pws_tests', _('Has access to PWS\'s Tests')),
            ('access_to_own_tests', _('Has access to own Tests')),
        )


class Letter(models.Model):
    site = models.ForeignKey(Site, blank=True, null=True, verbose_name=_("Site"), related_name="letters")
    letter_type = models.ForeignKey(LetterType, verbose_name=_("Letter Type"), related_name="letters")
    date = models.DateField(verbose_name=_("Send Date"), auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank=True, verbose_name=_("Sender"), related_name="letters")

    def __unicode__(self):
        return u"%s, %s" % (self.date, self.letter_type)

    class Meta:
        verbose_name = _("Letter")
        verbose_name_plural = _("Letters")
        permissions = (
            ('browse_letter', _('Can browse Letter')),
            ('send_letter', _('Can send Letter')),
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
    text = models.TextField(null=True, blank=True, verbose_name=_('Text'))

    def __unicode__(self):
        return u"%s" % self.title

    class Meta:
        verbose_name = _("Static Text")
        verbose_name_plural = _("Static Text")
