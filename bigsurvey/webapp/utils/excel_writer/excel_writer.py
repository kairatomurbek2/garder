from xlsxwriter import Workbook
from django.utils.translation import ugettext as _
from .parameters import SITE_FIELDS, HAZARD_FIELDS, BP_DEVICE_FIELDS, BOOLEAN_FIELDS, DATE_FIELDS
from main.settings import EXCEL_EXPORT_DIR, EXPORT_BASE_URL
from datetime import datetime
import os

SITE_FIELD_NAMES, SITE_FIELD_LABELS = zip(*SITE_FIELDS)
HAZARD_FIELD_NAMES, HAZARD_FIELD_LABELS = zip(*HAZARD_FIELDS)
BP_DEVICE_FIELD_NAMES, BP_DEVICE_FIELD_LABELS = zip(*BP_DEVICE_FIELDS)


class XLSExporter(object):
    def __init__(self, sites):
        self.file_name = 'Export_Services_%s.xlsx' % datetime.now().strftime("%Y-%m-%d-%s")
        self.file_uri = EXPORT_BASE_URL + self.file_name
        self.file_path = os.path.join(EXCEL_EXPORT_DIR, self.file_name)
        self.workbook = Workbook(self.file_path, {'constant_memory': True})
        self.current_sheet = self.workbook.add_worksheet(_("Sites"))
        self.sites = sites
        self.bold_style = self.workbook.add_format({'bold': True})
        self.row = 0
        self.col = 0

    def get_xls(self):
        self._write_headers()
        self._write_data()
        self.workbook.close()
        return self.file_uri

    def _write_headers(self):
        self._write_header_row(SITE_FIELD_LABELS)

    def _write_data(self):
        for site in self.sites:
            self._write_data_row(site, SITE_FIELD_NAMES)
            if site.hazards.all():
                self._write_separator_row()
                self._write_header_row(HAZARD_FIELD_LABELS, col=1)
                self._write_header_row(BP_DEVICE_FIELD_LABELS, same_row=True)
                for hazard in site.hazards.all():
                    self._write_data_row(hazard, HAZARD_FIELD_NAMES, col=1)
                    if hazard.bp_device:
                        self._write_data_row(hazard.bp_device, BP_DEVICE_FIELD_NAMES, same_row=True)
                self._write_separator_row()

    def _write_data_row(self, data_item, fields, col=0, same_row=False):
        if same_row:
            self.row -= 1
        else:
            self.col = col

        for field_name in fields:
            field = getattr(data_item, field_name)
            value = self._get_field_value(field, field_name)
            self.current_sheet.write(self.row, self.col, value)
            self.col += 1
        self.row += 1

    def _write_header_row(self, headers, col=0, same_row=False):
        if same_row:
            self.row -= 1
        else:
            self.col = col

        for header in headers:
            self.current_sheet.write(self.row, self.col, header, self.bold_style)
            self.col += 1
        self.row += 1

    def _write_separator_row(self):
        self.row += 1

    def _get_field_value(self, field, field_name):
        if field is None:
            return u''
        if field_name in BOOLEAN_FIELDS:
            if field:
                return u'Yes'
            return u'No'
        if field_name in DATE_FIELDS:
            return u'%02d-%02d-%02d' % (field.year, field.month, field.day)
        return unicode(field)
