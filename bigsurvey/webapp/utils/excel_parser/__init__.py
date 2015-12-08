ALPHABET_LENGTH = 26
FINISHED = 100
DEFAULT_BULK_SIZE = 1000
DEFAULT_PROGRESS_UPDATE_STEP = 1000

FOREIGN_KEY_PATTERN = '%s_id'
CUST_NUMBER_FIELD_NAME = 'cust_number'
PWS_FIELD_NAME = 'pws'
FOREIGN_KEY_FIELDS = [PWS_FIELD_NAME, 'site_use', 'site_type', 'status', 'floors', 'interconnection_point', 'cust_code']
DATE_FIELDS = ['connect_date', 'next_survey_date', 'last_survey_date']
NUMERIC_FIELDS = ['meter_reading', ]


class RequiredValueIsEmptyError(Exception):
    pass


class DateFormatError(Exception):
    pass


class CustomerNumberError(Exception):
    pass


class ForeignKeyError(Exception):
    pass


class NumericValueError(Exception):
    pass


class ExcelValidationError(Exception):
    def __init__(self, required_value_errors, date_format_errors, customer_number_errors,
                 foreign_key_errors, numeric_errors):
        self.required_value_errors = required_value_errors
        self.date_format_errors = date_format_errors
        self.customer_number_errors = customer_number_errors
        self.foreign_key_errors = foreign_key_errors
        self.numeric_errors = numeric_errors


from excel_parser import *

