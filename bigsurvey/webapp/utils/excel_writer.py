import cStringIO
from xlwt import Workbook, XFStyle, Font
from django.utils.translation import ugettext as _
from main.parameters import SITE_FIELD_NAMES


class XLSExporter(object):
    def __init__(self, dataset):
        self.xls_file = cStringIO.StringIO()
        self.workbook = Workbook(encoding="utf-8")
        self.current_sheet = self.workbook.add_sheet(_("Report"))
        self.header_style = self._get_header_style()
        self.dataset = dataset
        self.fields = SITE_FIELD_NAMES

    def get_xls(self):
        self._write_headers()
        self._write_data()
        return self._get_xls_content()

    def _get_header_style(self):
        style = XFStyle()
        font = Font()
        font.bold = True
        style.font = font
        return style

    def _get_xls_content(self):
        self.workbook.save(self.xls_file)
        content = self.xls_file.getvalue()
        self.xls_file.close()
        return content

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
                print field_name
                try:
                    value = field.pk
                except AttributeError:
                    value = field
                self.current_sheet.write(row, col, value)
                col += 1
            row += 1
