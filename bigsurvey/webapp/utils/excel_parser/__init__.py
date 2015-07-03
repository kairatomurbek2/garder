

ALPHABET_LENGTH = 26
FINISHED = 100
DEFAULT_BULK_SIZE = 1000
DEFAULT_PROGRESS_UPDATE_STEP = 1000

FOREIGN_KEY_PATTERN = '%s_id'
CUST_NUMBER_FIELD_NAME = 'cust_number'
PWS_FIELD_NAME = 'pws'
FOREIGN_KEY_FIELDS = [PWS_FIELD_NAME, 'site_use', 'site_type', 'status', 'floors', 'interconnection_point', 'cust_code']
DATE_FIELDS = ['connect_date', 'next_survey_date', 'last_survey_date']


class DateFormatError(Exception):
    pass

from excel_parser import *

