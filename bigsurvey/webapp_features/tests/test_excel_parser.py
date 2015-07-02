from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from webapp.models import ImportLog, PWS, Site
from webapp.utils.excel_parser import ExcelParser, DateFormatError
import os
from django.conf import settings

IMPORT_MAPPINGS = {
    "cust_number": 0,
    "cust_city": 18,
    "city": 8,
    "cust_code": 2,
    "zip": 10,
    "street_number": 5,
    "meter_number": 12,
    "connect_date": 3,
    "route": 11,
    "meter_size": 13,
    "apt": 7,
    "cust_zip": 20,
    "state": 9,
    "meter_reading": 14,
    "address1": 6,
    "cust_address1": 16,
    "cust_name": 15,
    "cust_state": 19,
    "cust_address2": 17,
    "next_survey_date": 4
}
DATE_FORMAT = "%Y%m%d"


class TestExcelParser(TestCase):
    fixtures = ['data_base.json']
    excel_parser = None
    import_log = None

    def setUp(self):
        self.pws = PWS(number=1, name='TestPWS')
        self.pws.save()
        self.user = get_user_model().objects.create(username='test_user')
        self.import_log = ImportLog(pws=self.pws, user=self.user)
        self.import_log.save()

    def _create_excel_parser(self, filename):
        return ExcelParser(os.path.join(settings.STUB_FILES_DIR, filename))

    def test_file_parsed(self):
        self.excel_parser = self._create_excel_parser('file_for_import_unit_test.xlsx')
        self.excel_parser.parse_and_save(IMPORT_MAPPINGS.copy(), self.import_log.pk, DATE_FORMAT)
        self.assertEqual(2118, Site.objects.all().count())

    def test_foreign_key_error(self):
        self.excel_parser = self._create_excel_parser('foreign_key_error.xlsx')
        self.assertRaisesMessage(IntegrityError, 'Incorrect value in C7 cell. Available values are 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, but found 100', self.excel_parser.check_constraints, IMPORT_MAPPINGS.copy(), DATE_FORMAT)

    def test_incorrect_date_format_error(self):
        self.excel_parser = self._create_excel_parser('incorrect_date_format.xlsx')
        self.assertRaisesMessage(DateFormatError, 'Date in D6 cell does not match "%Y%m%d" format', self.excel_parser.check_constraints, IMPORT_MAPPINGS.copy(), DATE_FORMAT)

    def test_required_values_is_empty_error(self):
        self.excel_parser = self._create_excel_parser('required_value_is_empty.xlsx')
        self.assertRaisesMessage(IntegrityError, "Found empty value in A4 cell, please fill in this cell", self.excel_parser.check_constraints, IMPORT_MAPPINGS.copy(), DATE_FORMAT)

    def test_duplicate_customer_number_error(self):
        self.excel_parser = self._create_excel_parser('duplicate_cust_numbers.xlsx')
        self.assertRaisesMessage(IntegrityError, "Duplicate Customer Numbers found in A6 and A10 cells", self.excel_parser.check_constraints, IMPORT_MAPPINGS.copy(), DATE_FORMAT)

    def test_import_two_times(self):
        self.test_file_parsed()
        self.test_file_parsed()
        self.assertEqual(2118, Site.objects.all().count())

    def test_file_remove_existing(self):
        self.excel_parser = self._create_excel_parser('correct.xlsx')
        self.excel_parser.parse_and_save(IMPORT_MAPPINGS.copy(), self.import_log.pk, DATE_FORMAT)
        self.excel_parser = self._create_excel_parser('correct-new.xlsx')
        self.excel_parser.parse_and_save(IMPORT_MAPPINGS.copy(), self.import_log.pk, DATE_FORMAT)
        self.assertEqual(3, self.import_log.deactivated_sites.count())