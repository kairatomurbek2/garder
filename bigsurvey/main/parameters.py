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
    AIR_GAP = _('Air Gap')
    AVB = _('AVB')
    DC = _('DC')
    DCDA = _('DCDA')
    HBVB = _('HBVB')
    PVB = _('PVB')
    RP = _('RP')
    RPDA = _('RPDA')


BP_TYPE_CHOICES = (
    (BP_TYPE.AIR_GAP, BP_TYPE.AIR_GAP),
    (BP_TYPE.AVB, BP_TYPE.AVB),
    (BP_TYPE.DC, BP_TYPE.DC),
    (BP_TYPE.DCDA, BP_TYPE.DCDA),
    (BP_TYPE.HBVB, BP_TYPE.HBVB),
    (BP_TYPE.PVB, BP_TYPE.PVB),
    (BP_TYPE.RP, BP_TYPE.RP),
    (BP_TYPE.RPDA, BP_TYPE.RPDA),
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


# class Details:
# cv1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 18]
# rv = [1, 10, 3, 11, 5, 6, 12, 4, 18]
# cv2 = cv1
# pvb = [1, 2, 13, 14, 15, 16, 17, 12, 4, 18]


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

NEXT_DATE_FILTER_CHOICES = (
    ('all', _('All')),
    ('week', _('Next Week')),
    ('month', _('Next Month')),
    ('year', _('Next Year')),
)

PAST_DATE_FILTER_CHOICES = (
    ('all', _('All')),
    ('week', _('1 week')),
    ('month', _('1 month')),
    ('2months', _('2 months')),
    ('3months', _('3 months')),
    ('6months', _('6 months')),
    ('year', _('1 year')),
    ('never', _('Never')),
)

TESTER_ASSEMBLY_STATUSES = ['Installed', 'Replaced']


class Groups:
    superadmin = 'SuperAdministrators'
    admin = 'Administrators'
    surveyor = 'Surveyors'
    tester = 'Testers'


ADMIN_GROUPS = [Groups.admin, Groups.surveyor, Groups.tester]

EXCEL_EXTENSIONS = ['.xls', '.xlsx']

CREDIT_CARD_TYPE_CHOICES = (
    ('visa', 'Visa'),
    ('mastercard', 'MasterCard'),
    ('amex', 'Amex'),
    ('discover', 'Discover'),
)

OTHER = 'other'

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
        required_fields_not_filled = _('Please fill in all required fields marked by asterisk')
        duplicate_excel_fields = _('You have selected the same Excel field more than once')
        foreign_key_error = _('Incorrect value in %s cell. Available values are %s, but found %s')
        required_value_is_empty = _('Found empty value in %s cell, please fill in this cell')
        incorrect_date_format = _('Date in %s cell does not match "%s" format')
        duplicate_cust_numbers = _('Duplicate Customer Numbers found in %s and %s cells')
        import_was_finished = _('Import was finished. Added sites: %d, updated sites: %d, deactivated sites: %d. More information <a href="%s">here</a>.')

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
        cv1_replaced_details_not_provided = _('You should provide details you have replaced for Check Valve 1')
        cv2_replaced_details_not_provided = _('You should provide details you have replaced for Relief Valve')
        rv_replaced_details_not_provided = _('You should provide details you have replaced for Check Valve 2')
        pvb_replaced_details_not_provided = _('You should provide details you have replaced for Pressure Vacuum Breaker')
        payment_successful_singular = 'Payment was completed successfully. Test is now visible on the site.'
        payment_successful_plural = 'Payment was completed successfully. Tests are now visible on the site.'
        payment_failed = _('Some errors happened during the payment. Please try again later.')
        payment_cancelled = _('You have cancelled payment. You can pay later.')

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

    class Letter:
        adding_success = _('Letter was successfully created')
        adding_error = _('Error while submitting form')
        editing_success = _('Letter was successfully updated')
        editing_error = _('Error while submitting form')
        send_success = _('Letter was successfully sent')
        send_error = _('Error while sending letter')

    class LetterType:
        editing_success = _('Lettertype was successfully updated')
        editing_error = _('Error while submitting form')