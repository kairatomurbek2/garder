from xlsxwriter import Workbook
from django.utils.translation import ugettext as _
from main.parameters import SITE_FIELD_NAMES, SITE_BOOLEAN_FIELDS, SITE_DATE_FIELDS
from main.settings import EXCEL_EXPORT_DIR, EXPORT_BASE_URL
from datetime import datetime
import os


class XLSExporter(object):
    def __init__(self, dataset):
        self.file_name = 'Export_Services_%s.xlsx' % datetime.now().strftime("%Y-%m-%d-%s")
        self.file_uri = EXPORT_BASE_URL + self.file_name
        self.file_path = os.path.join(EXCEL_EXPORT_DIR, self.file_name)
        self.workbook = Workbook(self.file_path, {'constant_memory': True})
        self.current_sheet = self.workbook.add_worksheet(_("Sites"))
        self.dataset = dataset
        self.fields = SITE_FIELD_NAMES

    def get_xls(self):
        self._write_headers()
        self._write_data()
        return self.file_uri

    def _write_headers(self):
        col = 0
        bold = self.workbook.add_format({'bold': True})
        for field in self.fields:
            self.current_sheet.write(0, col, field, bold)
            col += 1

    def _write_data(self):
        row = 1
        for item in self.dataset:
            col = 0
            for field_name in self.fields:
                field = getattr(item, field_name)
                value = self._get_field_value(field, field_name)
                self.current_sheet.write(row, col, value)
                col += 1
            row += 1
        self.workbook.close()

    def _get_field_value(self, field, field_name):
        if field is None:
            return ''
        if field_name in SITE_BOOLEAN_FIELDS:
            if field:
                return 'Yes'
            return 'No'
        if field_name in SITE_DATE_FIELDS:
            return '%02d-%02d-%02d' % (field.year, field.month, field.day)
        return unicode(field)
