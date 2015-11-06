from xlwt import Workbook, XFStyle, Font
from django.utils.translation import ugettext as _
from main.parameters import SITE_FIELD_NAMES, SITE_BOOLEAN_FIELDS, SITE_DATE_FIELDS, YESNO_CHOICES
from main.settings import BASE_DIR
from datetime import datetime
import os


class XLSExporter(object):
    def __init__(self, dataset):
        self.file_name = os.path.join(BASE_DIR, 'uploads/excel_export/export_%s.xls' % datetime.now().strftime("%s"))
        self.xls_file = open(self.file_name, 'w')
        self.workbook = Workbook(encoding="utf-8")
        self.current_sheet = self.workbook.add_sheet(_("Report"))
        self.header_style = self._get_header_style()
        self.dataset = dataset
        self.fields = SITE_FIELD_NAMES

    def get_xls(self):
        self._write_headers()
        self._write_data()
        return self.file_name

    def _get_header_style(self):
        style = XFStyle()
        font = Font()
        font.bold = True
        style.font = font
        return style

    def _write_headers(self):
        col = 0
        for field in self.fields:
            self.current_sheet.write(0, col, field, self.header_style)
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
        self.workbook.save(self.xls_file)
        self.xls_file.close()

    def _get_field_value(self, field, field_name):
        if field is None:
            return ''
        if field_name in SITE_BOOLEAN_FIELDS:
            if field:
                return 'Yes'
            return 'No'
        if field_name in SITE_DATE_FIELDS:
            return field.strftime("%Y-%m-%d")
        return unicode(field)
