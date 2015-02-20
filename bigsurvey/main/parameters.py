from django.utils.translation import ugettext as _


YESNO_CHOICES = (
    (True, "Yes"),
    (False, "No"),
)

VALVE_LEAKED_CHOICES = (
    (True, "Leaked"),
    (False, "Closed"),
)

VALVE_OPENED_CHOICES = (
    (True, "Opened"),
    (False, "Closed"),
)

TEST_RESULT_CHOICES = (
    (True, "Passed"),
    (False, "Failed"),
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

DATE_FILTER_CHOICES = (
    ('all', 'All'),
    ('week', 'Next Week'),
    ('month', 'Next Month'),
    ('year', 'Next Year'),
)

TESTER_ASSEMBLY_STATUSES = ['Installed', 'Replaced']


class Groups:
    superadmin = 'SuperAdministrators'
    admin = 'Administrators'
    surveyor = 'Surveyors'
    tester = 'Testers'


ADMIN_GROUPS = [Groups.admin, Groups.surveyor, Groups.tester]


class Messages:
    class Site:
        adding_success = _('Site was successfully added')
        adding_error = _('Error while submitting form')
        editing_success = _('Site was successfully updated')
        editing_error = _('Error while submitting form')

    class BatchUpdate:
        success = _('Batch update successfully performed')
        error = _('Cannot perform batch update. Please provide date')

    class PWS:
        adding_success = _('PWS was successfully added')
        adding_error = _('Error while submitting form')
        editing_success = _('PWS was successfully updated')
        editing_error = _('Error while submitting form')

    class Customer:
        adding_success = _('Customer was successfully added')
        adding_error = _('Error while submitting form')
        editing_success = _('Customer was successfully updated')
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