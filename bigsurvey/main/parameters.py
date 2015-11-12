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

    DC_TYPES = [DC, DCDA]
    RP_TYPES = [RP, RPDA]
    STANDALONE_TYPES = [PVB, SVB]
    NOT_REQUIRE_TEST_TYPES = [AIR_GAP, AVB, HBVB]
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
    (True, "Cleaned only"),
    (False, "Replaced")
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

TESTER_ASSEMBLY_STATUSES = ['Installed', 'Replaced']


class Groups:
    superadmin = 'SuperAdministrators'
    admin = 'Administrators'
    surveyor = 'Surveyors'
    tester = 'Testers'
    pws_owner = 'PWSOwners'


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
    "pk",
    "pws",
    "connect_date",
    "address1",
    "address2",
    "street_number",
    "apt",
    "city",
    "state",
    "zip",
    "site_use",
    "site_type",
    "status",
    "floors",
    "interconnection_point",
    "meter_number",
    "meter_size",
    "meter_reading",
    "route",
    "potable_present",
    "fire_present",
    "irrigation_present",
    "is_due_install",
    "is_backflow",
    "next_survey_date",
    "notes",
    "last_survey_date",
    "cust_number",
    "cust_name",
    "cust_code",
    "cust_address1",
    "cust_address2",
    "cust_apt",
    "cust_city",
    "cust_state",
    "cust_zip",
    "contact_phone",
    "contact_fax",
    "contact_email"
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

    class Site:
        adding_success = _('Site was successfully added')
        adding_error = _('Error while submitting form')
        editing_success = _('Site was successfully updated')
        editing_error = _('Error while submitting form')
        not_found = _('Site was not found')

    class Import:
        required_fields_not_filled = _('Please fill in all required fields marked by bold label')
        duplicate_excel_fields = _('You have selected the same Excel field more than once')
        foreign_key_error = _('Incorrect value in %s cell. Available values are %s, but found %s')
        required_value_is_empty = _('Found empty value in %s cell, please fill in this cell')
        incorrect_date_format = _('Date in %s cell does not match "%s" format')
        duplicate_cust_numbers = _('Duplicate Customer Numbers found in %s and %s cells')
        import_was_finished = _('Import was finished. Added sites: %d, updated sites: %d, deactivated sites: %d. More information <a href="%s">here</a>.')
        added_sites_header = _("You are browsing the sites that have been added during the import on %s")
        updated_sites_header = _("You are browsing the sites that have been updated during the import on %s")
        deactivated_sites_header = _("You are browsing the sites that have been deactivated during the import on %s")

    class BatchUpdate:
        success = _('Batch update was performed successfully')
        error = _('Cannot perform batch update. Please provide date.')

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

    class Test:
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
        assembly_type_not_set = _('You are now unable to add the test for this hazard because hazard does not have "Assembly Type Required" set. Please provide it <a href="%s">here</a>')

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
