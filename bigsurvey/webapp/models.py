from django.db import models
from django.utils.translation import ugettext_lazy as _
from main.parameters import *
from django.contrib.auth.models import User, Group


class SourceType(models.Model):
    source_type = models.CharField(max_length=50, verbose_name=_("Source Type"))

    def __unicode__(self):
        return self.source_type

    class Meta:
        verbose_name = _('Source Type')
        verbose_name_plural = _('Source Types')


class SiteType(models.Model):
    site_type = models.CharField(max_length=50, verbose_name=_("Site Type"))

    def __unicode__(self):
        return self.site_type

    class Meta:
        verbose_name = _('Site Type')
        verbose_name_plural = _('Site Types')


class SiteUse(models.Model):
    site_use = models.CharField(max_length=30, verbose_name=_("Site Use"))

    def __unicode__(self):
        return self.site_use

    class Meta:
        verbose_name = _('Site Use')
        verbose_name_plural = _('Site Use Types')


class ServiceType(models.Model):
    service_type = models.CharField(max_length=20, verbose_name=_("Service Type"))

    def __unicode__(self):
        return self.service_type

    class Meta:
        verbose_name = _('Service Type')
        verbose_name_plural = _('Service Types')


class SurveyType(models.Model):
    survey_type = models.CharField(max_length=20, verbose_name=_("Survey Type"))

    def __unicode__(self):
        return self.survey_type

    class Meta:
        verbose_name = _('Survey Type')
        verbose_name_plural = _('Survey Types')


class BPType(models.Model):
    bp_type = models.CharField(max_length=10, verbose_name=_("BFP Type"))

    def __unicode__(self):
        return self.bp_type

    class Meta:
        verbose_name = _('BFP Type')
        verbose_name_plural = _('BFP Types')


class BPSize(models.Model):
    bp_size = models.CharField(max_length=10, verbose_name=_("BFP Size"))

    def __unicode__(self):
        return self.bp_size

    class Meta:
        verbose_name = _('BFP Size')
        verbose_name_plural = _('BFP Sizes')


class BPManufacturer(models.Model):
    bp_manufacturer = models.CharField(max_length=30, verbose_name=_("BFP Manufacturer"))

    def __unicode__(self):
        return self.bp_manufacturer

    class Meta:
        verbose_name = _('BFP Manufacturer')
        verbose_name_plural = _('BFP Manufacturers')


class CustomerCode(models.Model):
    customer_code = models.CharField(max_length=20, verbose_name=_("Customer Code"))

    def __unicode__(self):
        return self.customer_code

    class Meta:
        verbose_name = _('Customer Code')
        verbose_name_plural = _('Customer Codes')


class HazardType(models.Model):
    hazard_type = models.CharField(max_length=50, verbose_name=_("Hazard Type"))

    def __unicode__(self):
        return self.hazard_type

    class Meta:
        verbose_name = _('Hazard Type')
        verbose_name_plural = _('Hazard Types')


class TestManufacturer(models.Model):
    test_manufacturer = models.CharField(max_length=20, verbose_name=_("Test Manufacturer"))

    def __unicode__(self):
        return self.test_manufacturer

    class Meta:
        verbose_name = _('Test Manufacturer')
        verbose_name_plural = _('Test Manufacturers')


class ICPointType(models.Model):
    ic_point = models.CharField(max_length=20, verbose_name=_("Interconnection Point"))

    def __unicode__(self):
        return self.ic_point

    class Meta:
        verbose_name = _('Interconnection Point Type')
        verbose_name_plural = _('Interconnection Point Types')


class AssemblyLocation(models.Model):
    assembly_location = models.CharField(max_length=20, verbose_name=_("Assembly Location"))

    def __unicode__(self):
        return self.assembly_location

    class Meta:
        verbose_name = _('Assembly Location')
        verbose_name_plural = _('Assembly Locations')


class LetterType(models.Model):
    letter_type = models.CharField(max_length=20, verbose_name=_("Letter Type"))
    template = models.TextField(max_length=2000, blank=True, null=True, verbose_name=_('Letter Template'))

    def __unicode__(self):
        return self.letter_type

    class Meta:
        verbose_name = _('Letter Type')
        verbose_name_plural = _('Letter Types')


class FloorsCount(models.Model):
    floors_count = models.CharField(max_length=10, verbose_name=_("Floors Count"))

    def __unicode__(self):
        return self.floors_count

    class Meta:
        verbose_name = _('Floors Count')
        verbose_name_plural = _('Floors Count')


class Special(models.Model):
    special = models.CharField(max_length=5, verbose_name=_("Special"))

    def __unicode__(self):
        return self.special

    class Meta:
        verbose_name = _('Special')
        verbose_name_plural = _('Special')


class Orientation(models.Model):
    orientation = models.CharField(max_length=15, verbose_name=_("Orientation"))

    def __unicode__(self):
        return self.orientation

    class Meta:
        verbose_name = _('Orientation Type')
        verbose_name_plural = _('Orientation Types')


class Employee(models.Model):
    user = models.OneToOneField(User)
    address = models.CharField(max_length=50, verbose_name=_("Address"))
    city = models.CharField(max_length=30, verbose_name=_("City"))
    state = models.CharField(max_length=2, choices=STATES, verbose_name=_("State"))
    zip = models.CharField(max_length=10, verbose_name=_("ZIP"))
    company = models.CharField(max_length=30, verbose_name=_("Company"))
    phone1 = models.CharField(max_length=20, verbose_name=_("Phone 1"))
    phone2 = models.CharField(blank=True, null=True, max_length=20, verbose_name=_("Phone 2"))
    fax = models.CharField(blank=True, null=True, max_length=20, verbose_name=_("Fax"))
    pws = models.ForeignKey(PWS, blank=True, null=True, verbose_name=_("PWS"), related_name="employees")


class Customer (models.Model):
    number = models.CharField(max_length=15, verbose_name=_("Number"))
    name = models.CharField(max_length=50, verbose_name=_("Name"))
    code = models.ForeignKey(CustomerCode, verbose_name=_("Customer Code"), related_name="customers")
    address1 = models.CharField(max_length=30, verbose_name=_("Address 1"))
    address2 = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Address 2"))
    apt = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("Customer Apt"))
    city = models.CharField(max_length=30, verbose_name=_("City"))
    state = models.CharField(max_length=2, choices=STATES, verbose_name=_("State"))
    zip = models.CharField(max_length=5, verbose_name=_("ZIP"))
    phone = models.CharField(max_length=10, blank=True, null=True, verbose_name=_("Phone"))
    notes = models.TextField(max_length=255, blank=True, null=True, verbose_name=_("Notes"))

    def __unicode__(self):
        return "%s (%s, %s)" % (self.name, self.city, self.state)

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')


class PWS (models.Model):
    number = models.CharField(max_length=15, verbose_name=_("Number"))
    name = models.CharField(max_length=50, verbose_name=_("Name"))
    city = models.CharField(max_length=30, verbose_name=_("City"))
    water_source = models.ForeignKey(SourceType, verbose_name=_("Water Source"), related_name="pws")
    notes = models.TextField(max_length=255, blank=True, null=True, verbose_name=_("Notes"))

    def __unicode__(self):
        return self.name + ", " + self.city

    class Meta:
        verbose_name = _('Public Water System')
        verbose_name_plural = _('Public Water Systems')


class Site(models.Model):
    customer = models.ForeignKey(Customer, verbose_name=_("Customer"), related_name="sites")
    pws = models.ForeignKey(PWS, verbose_name=_("PWS"), related_name="sites")
    connect_date = models.DateField(null=True, blank=True, verbose_name=_("Connect Date"))
    address = models.CharField(max_length=30, verbose_name=_("Address"))
    street_address = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Street Address"))
    street_number = models.CharField(max_length=10, blank=True, null=True, verbose_name=_("Street Number"))
    apt = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("Apt"))
    city = models.CharField(max_length=30, verbose_name=_("City"))
    state = models.CharField(max_length=2, choices=STATES, verbose_name=_("State"))
    zip = models.CharField(max_length=10, verbose_name=_("ZIP"))
    site_use = models.ForeignKey(SiteUse, verbose_name=_("Site Use"), related_name="sites")
    site_type = models.ForeignKey(SiteType, verbose_name=_("Site Type"), related_name="sites")
    floors = models.ForeignKey(FloorsCount, verbose_name=_("Building Height"), related_name="sites")
    interconnection_point = models.ForeignKey(ICPointType, verbose_name=_("Interconnection Point"),
                                              related_name="sites")
    potable_present = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Potable Present"))
    fire_present = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Fire Present"))
    irrigation_present = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Irrigation Present"))
    is_due_install = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Is Due Install"))
    is_backflow = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Is Backflow Present"))
    next_survey_date = models.DateField(null=True, blank=True, verbose_name=_("Next Survey Date"))
    notes = models.TextField(max_length=255, blank=True, null=True, verbose_name=_("Notes"))

    def __unicode__(self):
        return "%s, %s (%s)" % (self.street_address, self.street_number, self.PWS)

    class Meta:
        verbose_name = _("Site")
        verbose_name_plural = _("Sites")


class Service(models.Model):
    site = models.ForeignKey(Site, verbose_name=_("Site"), related_name="services")
    service_type = models.ForeignKey(ServiceType, verbose_name=_("Service Type"), related_name="services")
    notes = models.TextField(max_length=255, blank=True, null=True, verbose_name=_("Notes"))

    def __unicode__(self):
        return "%s, %s" % (self.site, self.service_type)

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")


class Survey(models.Model):
    service = models.ForeignKey(Service, verbose_name=_("Service"), related_name="surveys")
    survey_date = models.DateTimeField(verbose_name=_("Survey Date"))
    survey_type = models.ForeignKey(SurveyType, verbose_name=_("Survey Type"), related_name="surveys")
    surveyor = models.ForeignKey(User, null=True, blank=True, verbose_name=_("Surveyor"), related_name="surveys")
    metered = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Metered"))
    meter_number = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("Meter Number"))
    meter_size = models.CharField(max_length=15, blank=True, null=True, verbose_name=_("Meter Size"))
    meter_reading = models.FloatField(blank=True, null=True, verbose_name=_("Meter Reading"))
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
        return "%s, %s" % (self.survey_date, self.survey_type)

    class Meta:
        verbose_name = _("Survey")
        verbose_name_plural = _("Surveys")


class Hazard(models.Model):
    survey = models.ForeignKey(Survey, verbose_name=_("Survey"), related_name="hazards")
    hazard_type = models.ForeignKey(HazardType, verbose_name=_("Hazard Type"), related_name="hazards")
    BPPresent = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Is BP Present"))
    assembly_location = models.ForeignKey(AssemblyLocation, null=True, blank=True, verbose_name=_("Assembly Location"),
                                          related_name="hazards")
    assembly_status = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Assembly Status"))
    installer = models.CharField(max_length=30, blank=True, null=True, verbose_name=_("Installer"))
    install_date = models.DateTimeField(blank=True, null=True, verbose_name=_("Install Date"))
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
    notes = models.TextField(max_length=255, blank=True, null=True, verbose_name=_("Notes"))

    def __unicode__(self):
        return "%s, %s" % (self.assembly_location.assembly_location, self.hazard_type)

    class Meta:
        verbose_name = _("Hazard")
        verbose_name_plural = _("Hazards")


class Test(models.Model):
    bp_device = models.ForeignKey(Hazard, verbose_name=_("BP Device"),
                                  related_name="tests")
    test_serial_number = models.CharField(max_length=20, verbose_name=_("Test Serial No."))
    test_manufacturer = models.ForeignKey(TestManufacturer, verbose_name=_("Test Manufacturer"), related_name="tests")
    last_calibration_date = models.DateField(verbose_name=_("Last Calibration Date"))
    tester = models.ForeignKey(User, null=True, blank=True, verbose_name=_("Tester"), related_name="tests")
    tester_certificate = models.CharField(max_length=15, verbose_name=_("Tester Certificate No."))
    test_date = models.DateField(verbose_name=_("Test Date"), auto_now_add=True)
    next_test_date = models.DateField(null=True, blank=True, verbose_name=_("Next Test Date"))
    cv1_leaked = models.BooleanField(default=False, choices=VALVE_LEAKED_CHOICES, verbose_name=_("Leaked"))
    cv1_gauge_pressure = models.FloatField(blank=True, null=True, verbose_name=_("Gauge Pressure"))
    cv1_maintenance = models.BooleanField(default=False, choices=YESNO_CHOICES, verbose_name=_("Maintenance"))
    cv1_maintenance_pressure = models.FloatField(blank=True, null=True, verbose_name=_("Maintenance Pressure"))
    cv2_leaked = models.BooleanField(default=False, choices=VALVE_LEAKED_CHOICES, verbose_name=_("Leaked"))
    cv2_gauge_pressure = models.FloatField(blank=True, null=True, verbose_name=_("Gauge Pressure"))
    cv2_maintenance = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Maintenance"))
    cv2_maintenance_pressure = models.FloatField(null=True, blank=True, verbose_name=_("Maintenance Pressure"))
    rv_opened = models.BooleanField(choices=VALVE_OPENED_CHOICES, default=False, verbose_name=_("Opened"))
    rv_psi1 = models.FloatField(null=True, blank=True, verbose_name=_("Pressure 1"))
    rv_psi2 = models.FloatField(null=True, blank=True, verbose_name=_("Pressure 2"))
    rv_maintenance = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Maintenance"))
    outlet_sov_leaked = models.BooleanField(choices=VALVE_LEAKED_CHOICES, default=False, verbose_name=_("Leaked"))
    pvb_opened = models.BooleanField(choices=VALVE_OPENED_CHOICES, default=False, verbose_name=_("PVB Opened"))
    pvb_open_pressure = models.FloatField(null=True, blank=True, verbose_name=_("Open Pressure"))
    cv_leaked = models.BooleanField(choices=VALVE_LEAKED_CHOICES, default=False, verbose_name=_("Leaked"))
    cv_held_pressure = models.FloatField(null=True, blank=True, verbose_name=_("Held Pressure"))
    cv_maintenance = models.BooleanField(choices=YESNO_CHOICES, default=False, verbose_name=_("Maintenance"))
    air_inlet_psi = models.FloatField(null=True, blank=True, verbose_name=_("Air Inlet PSI"))
    cv_psi = models.FloatField(null=True, blank=True, verbose_name=_("Check Valve PSI"))
    test_result = models.BooleanField(choices=TEST_RESULT_CHOICES, default=False, verbose_name=_("Test Result"))
    notes = models.TextField(max_length=255, blank=True, null=True, verbose_name=_("Notes"))

    def __unicode__(self):
        return "%s, %s" % (self.bp_device.assembly_location, self.test_date)

    class Meta:
        verbose_name = _("Test")
        verbose_name_plural = _("Tests")


class Letter(models.Model):
    survey = models.ForeignKey(Survey, verbose_name=_("Survey"), related_name="letters")
    letter_type = models.ForeignKey(LetterType, verbose_name=_("Letter Type"), related_name="letters")
    date = models.DateTimeField(verbose_name=_("Send Date"), auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank=True, verbose_name=_("Sender"), related_name="letters")

    def __unicode__(self):
        return "%s, %s" % (self.date, self.letter_type)

    class Meta:
        verbose_name = _("Letter")
        verbose_name_plural = _("Letters")


class Licence(models.Model):
    given_to = models.ForeignKey(User, verbose_name=_("Given To"), related_name="licences")
    given_by = models.ForeignKey(User, null=True, blank=True, verbose_name=_("Given By"), related_name="licences_given")
    start_date = models.DateField(verbose_name=_("Start Date"))
    end_date = models.DateField(verbose_name=_("End Date"))
    is_active = models.BooleanField(verbose_name=_("Is Active"))
    notes = models.TextField(max_length=255, blank=True, null=True, verbose_name=_("Notes"))

    def __unicode__(self):
        return "%s, %s" % (self.given_to.name, self.start_date)

    class Meta:
        verbose_name = "Licence"
        verbose_name_plural = "Licences"


class TestPermission(models.Model):
    site = models.ForeignKey(Site, verbose_name=_("Site"), related_name="test_perms")
    given_to = models.ForeignKey(User, verbose_name=_("Given To"), related_name='test_perms_granted')
    given_by = models.ForeignKey(User, null=True, blank=True, verbose_name=_("Given By"),
                                 related_name='test_perms_given')
    given_date = models.DateField(verbose_name=_("Given Date"), auto_now_add=True)
    due_date = models.DateField(verbose_name=_("Due Date"))
    is_active = models.BooleanField(verbose_name=_("Is Active"), default=True)
    notes = models.TextField(max_length=255, blank=True, null=True, verbose_name=_("Notes"))

    def __unicode__(self):
        return "%s %s, %s" % (self.given_to.first_name, self.given_to.last_name, self.given_date)

    class Meta:
        verbose_name = "Test Permission"
        verbose_name_plural = "Test Permissions"


class Inspection(models.Model):
    site = models.ForeignKey(Site, verbose_name=_("Site"), related_name='inspections')
    assigned_to = models.ForeignKey(User, verbose_name=_("Assigned To"), related_name='inspections')
    assigned_by = models.ForeignKey(User, null=True, blank=True, verbose_name=_("Assigned By"),
                                    related_name='inspects_assigned')
    assigned_date = models.DateField(verbose_name=_("Assigned Date"), auto_now_add=True)
    is_active = models.BooleanField(verbose_name=_("Is Active"), default=True)
    notes = models.TextField(max_length=255, blank=True, null=True, verbose_name=_("Notes"))

    def __unicode__(self):
        return "%s %s, %s" % (self.assigned_to.first_name, self.assigned_to.last_name, self.assigned_date)

    class Meta:
        verbose_name = "Inspection"
        verbose_name_plural = "Inspections"