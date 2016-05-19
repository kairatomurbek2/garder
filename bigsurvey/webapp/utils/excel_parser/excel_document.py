import xlsxwriter
import xlrd
from xlrd.biffh import XL_CELL_NUMBER, XL_CELL_TEXT
from django.utils.translation import ugettext as _

EXCEL_MODE_READ = 1
EXCEL_MODE_WRITE = 2
EXCEL_WRITE_STYLE_NORMAL = 1
EXCEL_WRITE_STYLE_BOLD = 2
EXCEL_WRITE_STYLE_ITALIC = 3


class ExcelDocument(object):
    def __init__(self, filename, mode, header_row=0):
        self.filename = filename
        self._mode = mode
        self._current_row = -1
        self._current_style = EXCEL_WRITE_STYLE_NORMAL
        self._workbook = None
        self._sheet = None
        self._bold_style = None
        self._italic_style = None
        self._header_row = header_row
        self._headers = None
        self.row_count = 0
        if self._mode == EXCEL_MODE_READ:
            self._open_for_read()
        else:
            self._open_for_write()

    def _open_for_read(self):
        self._workbook = xlrd.open_workbook(self.filename)
        self._sheet = self._workbook.sheet_by_index(0)
        self.row_count = self._sheet.nrows
        self._parse_headers()

    def _parse_headers(self):
        self._headers = []
        for col in xrange(self._sheet.ncols):
            value = self.read_cell(self._header_row, col)
            if value:
                self._headers.append((col, value))

    def read_headers(self):
        return self._headers

    def read_n_rows(self, row_count, start_row=-1):
        start_row, row_count = self._fit_n_rows_parameters(row_count, start_row)
        rows = []
        for row in xrange(start_row, start_row + row_count):
            rows.append(self.read_row(row))
        return rows

    def read_n_headered_rows(self, row_count, start_row=-1):
        start_row, row_count = self._fit_n_rows_parameters(row_count, start_row)
        rows = []
        for row in xrange(start_row, start_row + row_count):
            rows.append(self.read_headered_row(row))
        return rows

    def _fit_n_rows_parameters(self, row_count, start_row):
        if start_row < 0:
            start_row = self._header_row + 1
        if row_count + start_row > self.row_count:
            row_count = self.row_count - start_row
        return start_row, row_count

    def read_next_row(self):
        self._current_row += 1
        if self._current_row < self.row_count:
            return self.read_row(self._current_row)
        return []

    def read_next_headered_row(self):
        self._current_row += 1
        if self._current_row < self.row_count:
            return self.read_headered_row(self._current_row)
        return []

    def read_headered_row(self, row):
        values = []
        for col, _ in self._headers:
            values.append(self.read_cell(row, col))
        return values

    def read_row(self, row):
        values = []
        for col in xrange(self._sheet.ncols):
            values.append(self.read_cell(row, col))
        return values

    def read_cell(self, row, column):
        cell = self._sheet.cell(row, column)
        if cell.ctype == XL_CELL_TEXT:
            return cell.value.strip()
        if cell.ctype == XL_CELL_NUMBER:
            return int(cell.value)
        return cell.value

    def _open_for_write(self):
        self._workbook = xlsxwriter.Workbook(self.filename, {'constant_memory': True})
        self._sheet = self._workbook.add_worksheet(_("Duplicates"))
        self._bold_style = self._workbook.add_format({'bold': True})
        self._italic_style = self._workbook.add_format({'italic': True})

    def write_next_row(self, *values):
        self._current_row += 1
        self.write_row(self._current_row, *values)

    def write_row(self, row, *values):
        column = 0
        for item in values:
            self.write_cell(row, column, item)
            column += 1

    def write_cell(self, row, column, value):
        self._sheet.write(row, column, value, self._current_style)

    def set_write_style(self, style):
        if style == EXCEL_WRITE_STYLE_BOLD:
            self._current_style = self._bold_style
        elif style == EXCEL_WRITE_STYLE_ITALIC:
            self._current_style = self._italic_style
        else:
            self._current_style = None

    def close(self, save=True):
        if not save:
            self._workbook.fileclosed = 1
        self._workbook.close()

    def reset_current_row(self):
        self._current_row = -1

    @property
    def current_row(self):
        return self._current_row

    @property
    def header_row(self):
        return self._header_row
