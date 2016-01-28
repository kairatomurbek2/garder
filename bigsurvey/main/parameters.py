from django.utils.translation import ugettext as _


class SERVICE_TYPE(object):
    POTABLE = "potable"
    FIRE = "fire"
    IRRIGATION = "irrigation"


class SITE_STATUS(object):
    ACTIVE = 'Active'
    SUSPENDED = 'Suspended'
    DISCONNECTED = 'Disconnected'
    INACTIVE = 'Inactive'


class BP_TYPE(object):
    AIR_GAP = 'Air Gap'
    AVB = 'AVB'
    DC = 'DC'
    DCDA = 'DCDA'
    HBVB = 'HBVB'
    PVB = 'PVB'
    RP = 'RP'
    RPDA = 'RPDA'
    SVB = 'SVB'
    UNKNOWN = 'Unknown'

    DC_TYPES = [DC, DCDA]
    RP_TYPES = [RP, RPDA]
    STANDALONE_TYPES = [PVB, SVB]
    NOT_REQUIRE_TEST_TYPES = [AIR_GAP, AVB, HBVB, UNKNOWN]
    REQUIRE_TEST_TYPES = [DC, DCDA, PVB, RP, RPDA, SVB]

BP_TYPE_CHOICES = (
    (BP_TYPE.AIR_GAP, BP_TYPE.AIR_GAP),
    (BP_TYPE.AVB, BP_TYPE.AVB),
    (BP_TYPE.DC, BP_TYPE.DC),
    (BP_TYPE.DCDA, BP_TYPE.DCDA),
    (BP_TYPE.HBVB, BP_TYPE.HBVB),
    (BP_TYPE.PVB, BP_TYPE.PVB),
    (BP_TYPE.RP, BP_TYPE.RP),
    (BP_TYPE.RPDA, BP_TYPE.RPDA),
    (BP_TYPE.SVB, BP_TYPE.SVB),
    (BP_TYPE.UNKNOWN, BP_TYPE.UNKNOWN)
)


class LetterTypes(object):
    DUE_INSTALL_FIRST = 'Due Install First'
    DUE_INSTALL_SECOND = 'Due Install Second'
    DUE_INSTALL_THIRD = 'Due Install Third'
    ANNUAL_TEST_FIRST = 'Annual Test First'
    ANNUAL_TEST_SECOND = 'Annual Test Second'
    ANNUAL_TEST_THIRD = 'Annual Test Third'


class BPLocations(object):
    INTERNAL = 'Internal'
    AT_METER = 'At Meter'


class AssemblyStatus(object):
    INSTALLED = 'installed'
    DUE_INSTALL = 'due_install'
    DUE_REPLACE = 'due_replace'
    NOT_REQUIRED = 'not_required'
    MAINTENANCE = 'maintenance'

ASSEMBLY_STATUS_CHOICES = (
    (AssemblyStatus.INSTALLED, _('Installed')),
    (AssemblyStatus.DUE_INSTALL, _('Due Install')),
    (AssemblyStatus.DUE_REPLACE, _('Due Replace')),
    (AssemblyStatus.MAINTENANCE, _('Maintenance')),
    (AssemblyStatus.NOT_REQUIRED, _('Not Required'))
)

ASSEMBLY_STATUSES_WITH_BP = (
    AssemblyStatus.INSTALLED,
    AssemblyStatus.DUE_REPLACE,
    AssemblyStatus.MAINTENANCE
)

YESNO_CHOICES = (
    (True, "Yes"),
    (False, "No"),
)

VALVE_LEAKED_CHOICES = (
    (True, "Leaked"),
    (False, "Closed Tight"),
)

VALVE_OPENED_CHOICES = (
    (True, "Opened"),
    (False, "Closed"),
)

TEST_RESULT_CHOICES = (
    (True, "Passed"),
    (False, "Failed"),
)

CLEANED_REPLACED_CHOICES = (
    ("0", _("Tested Only")),
    ("1", _("Cleaned only")),
    ("2", _("Maintenance"))

)

STATES = (
    ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'),
    ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'),
    ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'),
    ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'),
    ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'),
    ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'),
    ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'),
    ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'),
    ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming'),
)

STATES_FILTER = (
    ('', 'All'), ('blank', 'Blank'), ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'),
    ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'),
    ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'),
    ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'),
    ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'),
    ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'),
    ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'),
    ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'),
    ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming'),
)

NEXT_DATE_FILTER_CHOICES = (
    ('all', _('All')),
    ('blank', _('Blank')),
    ('past', _('Past')),
    ('today', _('Today')),
    ('week', _('Next week')),
    ('month', _('Next month')),
    ('year', _('Next year')),
)

PAST_DATE_FILTER_CHOICES = (
    ('all', _('All')),
    ('blank', _('Blank')),
    ('week', _('Last week')),
    ('month', _('Last month')),
    ('1-2months', _('1-2 months ago')),
    ('2-3months', _('2-3 months ago')),
    ('3-4months', _('3-6 months ago')),
    ('6-12months', _('6-12 months ago')),
    ('year', _('Over a year ago')),
)


class Groups:
    superadmin = 'SuperAdministrators'
    admin = 'Administrators'
    surveyor = 'Surveyors'
    tester = 'Testers'
    pws_owner = 'PWSOwners'
    ad_auth = 'Administrative Authority'


ADMIN_GROUPS = [Groups.admin, Groups.surveyor, Groups.tester]

OWNER_GROUPS = [Groups.pws_owner, Groups.admin, Groups.surveyor, Groups.tester]

EXCEL_EXTENSIONS = ['.xls', '.xlsx']

CREDIT_CARD_TYPE_CHOICES = (
    ('visa', 'Visa'),
    ('mastercard', 'MasterCard'),
    ('amex', 'Amex'),
    ('discover', 'Discover'),
)

OTHER = 'other'

SITE_FIELD_NAMES = [
    ("pk", "ID"),
    ("pws", "PWS"),
    ("connect_date", "Connect Date"),
    ("status", "Site Status"),
    ("cust_number", "Account Number"),
    ("cust_code", "Customer Code"),
    ("last_survey_date", "Last Survey Date"),
    ("next_survey_date", "Next Survey Date"),
    ("due_install_test_date", "Due Install/Test Date"),
    ("route", "Seq. Route"),
    ("address1", "Service Address 1"),
    ("address2", "Service Address 2"),
    ("street_number", "Service Street Number"),
    ("apt", "Service Apt."),
    ("city", "Service City"),
    ("state", "Service State"),
    ("zip", "Service ZIP"),
    ("site_use", "Site Use"),
    ("site_type", "Site Type"),
    ("floors", "Floors Count"),
    ("interconnection_point", "Interconnection Point"),
    ("meter_number", "Meter Number"),
    ("meter_size", "Meter Size"),
    ("meter_reading", "Meter Reading"),
    ("potable_present",  "Potable Present"),
    ("fire_present", "Fire Present"),
    ("irrigation_present", "Irrigation Present"),
    ("is_due_install", "Is Due Install"),
    ("is_backflow", "Is Backflow"),
    ("cust_address1", "Customer Address 1"),
    ("cust_address2", "Customer Address 2"),
    ("cust_apt", "Customer Apt."),
    ("cust_city", "Customer City"),
    ("cust_state", "Customer State"),
    ("cust_zip", "Customer ZIP"),
    ("cust_name", "Customer Name"),
    ("contact_phone", "Contact Phone"),
    ("contact_fax", "Contact FAX"),
    ("contact_email", "Contact Email"),
    ("notes", "Notes"),
]

SITE_BOOLEAN_FIELDS = [
    "potable_present",
    "fire_present",
    "irrigation_present",
    "is_due_install",
    "is_backflow",
]

SITE_DATE_FIELDS = [
    "connect_date",
    "next_survey_date",
    "last_survey_date",
]

DATEFORMAT_CHOICES = (
    ('%Y-%m-%d', '%Y-%m-%d'),
    ('%m/%d/%Y', '%m/%d/%Y'),
    ('%m/%d/%y', '%m/%d/%y'),
    ('%b %d %Y', '%b %d %Y'),
    ('%b %d, %Y', '%b %d, %Y'),
    ('%d %b %Y', '%d %b %Y'),
    ('%d %b, %Y', '%d %b, %Y'),
    ('%B %d %Y', '%B %d %Y'),
    ('%B %d, %Y', '%B %d, %Y'),
    ('%d %B %Y', '%d %B %Y'),
    ('%d %B, %Y', '%d %B, %Y'),
    (OTHER, 'Other'),
)

DATEFORMAT_HELP = (
    {
        'code': '%d',
        'meaning': _('Day of the month as a zero-padded decimal number.'),
        'example': '03',
    },
    {
        'code': '%-d',
        'meaning': _('Day of the month as a decimal number. (Platform specific)'),
        'example': '3',
    },
    {
        'code': '%b',
        'meaning': _('Month as locale\'s abbreviated name.'),
        'example': 'Sep',
    },
    {
        'code': '%B',
        'meaning': _('Month as locale\'s full name.'),
        'example': 'September',
    },
    {
        'code': '%m',
        'meaning': _('Month as a zero-padded decimal number.'),
        'example': '09',
    },
    {
        'code': '%-m',
        'meaning': _('Month as a decimal number. (Platform specific)'),
        'example': '9',
    },
    {
        'code': '%y',
        'meaning': _('Year without century as a zero-padded decimal number.'),
        'example': '13',
    },
    {
        'code': '%Y',
        'meaning': _('Year with century as a decimal number.'),
        'example': '2013',
    },
)


class Messages:
    extension_not_allowed = _('File extension is not allowed. Allowed extensions: %(allowed_extensions)s')
    form_error = _('Error while submitting form')

    class Site:
        adding_success = _('Site was successfully added')
        adding_error = _('Error while submitting form')
        editing_success = _('Site was successfully updated')
        editing_error = _('Error while submitting form')
        not_found = _('Site was not found')
        search_error_fields_not_filled = _("Besides PWS, at least one of the following fields must be filled: %s")
        search_error_more_than_one_field_filled = _("Besides PWS, only one of the following fields can be filled: %s")
        search_server_error = _("Search engine error occurred. Please, contact site admin.")
        account_number_exists = _("There is already a site with this account number")

    class Import:
        required_fields_not_filled = _('Please fill in all required fields marked by bold label')
        duplicate_excel_fields = _('You have selected the same Excel field more than once')
        foreign_key_error = _('Incorrect value in %s cell. Available values are %s, but found %s')
        required_value_is_empty = _('Found empty value in %s cell, please fill in this cell')
        incorrect_date_format = _('Date in %s cell does not match "%s" format')
        incorrect_numeric_value = _('Cell %s should contain number or empty value')
        duplicate_cust_numbers = _('Duplicate Customer Numbers found in %s and %s cells')
        import_was_finished = _('Import was finished. Added sites: %d, updated sites: %d, deactivated sites: %d. More information <a href="%s">here</a>.')
        added_sites_header = _("You are browsing the sites that have been added during the import on %s")
        updated_sites_header = _("You are browsing the sites that have been updated during the import on %s")
        deactivated_sites_header = _("You are browsing the sites that have been deactivated during the import on %s")

    class BatchUpdate:
        success = _('Batch update was performed successfully')
        error = _('Cannot perform batch update. Please, provide date or select "Empty Date" option')
        error_date_in_future = _('Cannot perform batch update. Please, provide current date or date in the past')

    class PWS:
        adding_success = _('PWS was successfully added')
        adding_error = _('Error while submitting form')
        editing_success = _('PWS was successfully updated')
        editing_error = _('Error while submitting form')

    class Survey:
        adding_success = _('Survey was successfully added')
        adding_error = _('Error while submitting form')
        editing_success = _('Survey was successfully updated')
        editing_error = _('Error while submitting form')

    class Hazard:
        adding_success = _('Hazard was successfully added')
        adding_error = _('Error while submitting form')
        editing_success = _('Hazard was successfully updated')
        editing_error = _('Error while submitting form')
        device_absence_warning = _('Note: Hazard has Assembly Status "%s" but does not have BP-Device associated with it.')
        device_presence_warning = _('Note: Hazard has Assembly Status "%s", but has BP-Device associated with it.')
        hazard_inactive = _('Note: Hazard is marked as not present on site anymore. You can mark it as present by editing it.')

    class BPDevice:
        adding_success = _('Backflow Preventer was successfully created')
        editing_success = _('Backflow Preventer was successfully updated')

    class Test:
        cv_retest_psi_value_should_be = _('Check valve  psi value should be greater than or equal to 1')
        air_inlet_retest_psi_value_should_be = _('Air Inlet psi value should be greater than or equal to 1')
        cv_leaked_value_should_be = _('Or held at Valve psi should be greater than or equal to 1')
        air_inlet_psi_value_should_be = _('Opened at Valve psi value should be greater than or equal to 1')
        cv2_retest_gauge_pressure_value_should_be = _('Gauge pressure across Valve psi value should be greater than or equal to 1')
        rv_psi2_value_should_be = _('Relief valve opened at Valve psi value should be greater than or equal to 2')
        cv1_retest_gauge_pressure_value_should_be = _('Gauge pressure across Valve psi value should be greater than or equal to 5')
        cv2_gauge_pressure_value_should_be = _('Gauge pressure across Valve psi value should be greater than or equal to 1')
        outlet_sov_leaked_and_passed_error = _('You should either set "Outlet shut-off Valve" to "Leaked" and "Test result" to "Failed" or set "Outlet shut-off Valve" to "Closed Tight" and "Test result" to "Passed"')
        cv1_gauge_pressure_value_should_be = _('Gauge pressure across Valve psi value should be greater than or equal to 5')
        cv2_leaked_and_passed_error = _('You should either set "Check Valve #2" to "Leaked" and "Test result" to "Failed" or set "Check Valve #2" to "Closed Tight" and "Test result" to "Passed"')
        rv_psi1_value_should_be_gte_two = _('Relief Valve psi value should be greater than or equal to 2')
        adding_success = _('Test was successfully added')
        adding_error = _('Error while submitting form')
        editing_success = _('Test was successfully updated')
        editing_error = _('Error while submitting form')
        air_inlet_not_provided = _('You should either set "Air Inlet Did not open" or provide "Air Inlet psi"')
        rv_not_provided = _('You should either set "Relief Valve Did not open" or provide "Relief Valve psi"')
        cv_not_provided = _('You should either set "Check Valve Did not open" or provide "Check Valve psi"')
        cv1_replaced_details_not_provided = _('You must provide details for replacement of Check Valve #1')
        cv2_replaced_details_not_provided = _('You must provide details for replacement of Check Valve #2')
        rv_replaced_details_not_provided = _('You must provide details for replacement of Relief Valve')
        pvb_replaced_details_not_provided = _('You must provide details for replacement of Pressure Vacuum Breaker')
        payment_successful_singular = 'Payment was completed successfully. Test is now visible on the site.'
        payment_successful_plural = 'Payment was completed successfully. Tests are now visible on the site.'
        payment_failed = _('Some errors happened during the payment. Please try again later.')
        payment_cancelled = _('You have cancelled payment. You can pay later.')
        assembly_type_not_set = _('You are now unable to add the test for this hazard because hazard does not have "Assembly Type Present" set. Please provide it <a href="%s">here</a>')
        assembly_type_not_set_no_licence = _('You are now unable to add the test for this hazard because hazard does not have "Assembly Type Required" set. You are now unable to set "Assembly Type Required" because you do not have Licence for Installation. Please, contact your PWS administrator to resolve this issue.')
        cv1_leaked_and_passed_error = _('You should either set "Check Valve #1" to "Leaked" and "Test result" to "Failed" or set "Check Valve #1" to "Closed Tight" and "Test result" to "Passed"')

    class Inspection:
        adding_success = _('Inspection was successfully added')
        adding_error = _('Error while submitting form')
        editing_success = _('Inspection was successfully updated')
        editing_error = _('Error while submitting form')

    class TestPermission:
        adding_success = _('Test Permission was successfully added')
        adding_error = _('Error while submitting form')
        editing_success = _('Test Permission was successfully updated')
        editing_error = _('Error while submitting form')

    class User:
        adding_success = _('User was successfully added')
        adding_error = _('Error while submitting form')
        editing_success = _('User was successfully updated')
        editing_error = _('Error while submitting form')

    class TestKit:
        test_kit_add_success = _('Test Kit was successfully added')
        test_kit_edit_success = _('Test Kit was successfully updated')

    class TesterCert:
        tester_cert_add_success = _('Certificate was successfully added')
        tester_cert_edit_success = _('Certificate was successfully updated')

    class TesterInvite:
        tester_not_found = _('Tester with such email and certificate number not found')
        tester_already_in_pws = _('Selected tester is employee of your PWS already')
        tester_invite_error = _('Error while submitting form')
        tester_invite_success = _('Invite have been sent to selected tester\'s email. He should accept it in 3 days')
        tester_invite_failed = _('Failed to send invite. Please, try again later.')

    class Letter:
        adding_success = _('Letter was successfully created')
        adding_error = _('Error while submitting form')
        editing_success = _('Letter was successfully updated')
        editing_error = _('Error while submitting form')
        send_success = _('Letter was successfully sent')
        send_error = _('Error while sending letter')
        required_data_present = _("All required data is present!")
        fields_without_value = _("Following fields has no value in database: %s")
        letter_already_sent = _(
            "This letter has been sent already. If you have changed site or hazard data from this letter and want to send it again, please, open the letter in edit mode and submit the form to regenerate letter content.")

    class LetterType:
        editing_success = _('Lettertype was successfully updated')
        editing_error = _('Error while submitting form')


POSSIBLE_IMPORT_MAPPINGS = {
    "PWS": ('pws',),
    "Connect Date": ('connectdate', 'connectiondate',),
    "Service Street Address": ('streetaddress', 'sitestreetaddress', 'servicestreetaddress', 'sitestreet', 'servicestreet', 'siteaddress', 'serviceaddress', 'address1',),
    "Service Secondary Address": ('siteaddress2', 'serviceaddress2', 'address2',),
    "Service Street Number": ('sitestreetnumber', 'servicestreetnumber', 'streetnumber',),
    "Service Apt": ('siteapt', 'serviceapt', 'apt', 'apartment',),
    "Service City": ('sitecity', 'sitetown', 'servicecity', 'servicetown', 'city', 'town',),
    "Service State": ('servicestate', 'state', 'sitestate',),
    "Service ZIP": ('sitezip', 'servicezip', 'zip',),
    "Site Use": ('siteuse', 'serviceuse',),
    "Site Type": ('sitetype', 'servicetype',),
    "Site Status": ('sitestatus', 'servicestatus', 'status',),
    "Number of Floors": ('floorcount', 'buildingheight', 'countoffloors', 'floors',),
    "Interconnection Point": ('icpoint', 'icpointtype', 'interconnectionpoint', 'interconnection',),
    "Meter Number": ('meternumber',),
    "Meter Size": ('metersize',),
    "Meter Reading": ('meterreading', 'meterreadings', 'readings', 'reading',),
    "Sequence Route": ('seqroute', 'route', 'sequenceroute',),
    "Potable Present": ('potable', 'ispotable', 'potablepresent', 'ispotablepresent',),
    "Fire Present": ('fire', 'isfire', 'firepresent', 'isfirepresent',),
    "Irrigation Present": ('irrigation', 'isirrigation', 'irrigationpresent', 'isirrigationpresent',),
    "Is Due Install": ('isdueinstall',),
    "Is Backflow Present": ('isbackflow', 'isbackflowpresent',),
    "Next Survey Date": ('nextsurvey', 'nextsurveydate',),
    "Notes": ('notes', 'note',),
    "Last Survey Date": ('lastsurvey', 'lastsurveydate',),
    "Account Number": ('account', 'customeraccount', 'accountnumber', 'customernumber', 'custaccount', 'custnumber', 'customeraccountnumber', 'custaccountnumber',),
    "Customer Name": ('name', 'customername', 'custname',),
    "Customer Code": ('code', 'customercode', 'custcode',),
    "Customer Main Address": ('custaddress1', 'customeraddress1', 'custaddress', 'customeraddress',),
    "Customer Secondary Address": ('custaddress2', 'customeraddress2',),
    "Customer Apt": ('custapt', 'customerapt',),
    "Customer City": ('custcity', 'custtown', 'customercity', 'customertown',),
    "Customer State": ('custstate', 'customerstate',),
    "Customer ZIP": ('custzip', 'customerzip',),
    "Customer Phone": ('custphone', 'customerphone', 'phone', 'tel', 'telephone',),
    "Customer Fax": ('custfax', 'customerfax', 'fax',),
    "Customer Email": ('customeremail', 'custemail', 'email',),
    "Due Test Date": ('dueinstalltestdate', 'dueinstalldate', 'duetestdate', 'dueinstalltest', 'dueinstall', 'duetest', 'testduedate', 'installduedate',),
}
