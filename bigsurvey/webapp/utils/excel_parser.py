import os
from django.conf import settings
import xlrd


class ExcelParser(object):
    def __init__(self, filename, headers_row_number=0):
        self.book = xlrd.open_workbook(os.path.join(settings.MEDIA_ROOT, filename))
        self.sheet = self.book.sheet_by_index(0)
        self.headers_row_number = headers_row_number

    def get_headers_as_choices(self):
        headers = []
        for column_number in xrange(self.sheet.ncols):
            cell = self.sheet.cell(self.headers_row_number, column_number)
            if cell.value:
                headers.append((column_number, cell.value))
        return headers

    def get_example_rows(self, rows_count, headers):
        example_rows = []
        start_row_number = self.headers_row_number + 1
        for row_number in xrange(rows_count):
            actual_row_number = start_row_number + row_number
            row = []
            for column_number, field_name in headers:
                cell = self.sheet.cell(actual_row_number, column_number)
                row.append(cell.value)
            example_rows.append(row)
        return example_rows