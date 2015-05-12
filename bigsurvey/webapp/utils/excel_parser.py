import os
from datetime import datetime
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned
from django.db import IntegrityError
from django.db.models import NOT_PROVIDED
import xlrd
from xlrd.biffh import XL_CELL_NUMBER
from main.parameters import Messages
from webapp import models


class DateFormatError(Exception):
    pass


class ExcelParser(object):
    FOREIGN_KEY_PATTERN = '%s_id'
    CUST_NUMBER_FIELD_NAME = 'cust_number'
    PWS_FIELD_NAME = 'pws'
    FOREIGN_KEY_FIELDS = [PWS_FIELD_NAME, 'site_use', 'site_type', 'status', 'floors', 'interconnection_point', 'cust_code']
    DATE_FIELDS = ['connect_date', 'next_survey_date', 'last_survey_date']
    DATE_FORMAT = '%Y%m%d'

    def __init__(self, filename, headers_row_number=0):
        self.book = xlrd.open_workbook(os.path.join(settings.MEDIA_ROOT, filename), on_demand=True)
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
        for row_number in xrange(start_row_number, start_row_number + rows_count):
            row = []
            for column_number, field_name in headers:
                cell = self.sheet.cell(row_number, column_number)
                row.append(self._get_cell_value(cell))
            example_rows.append(row)
        return example_rows

    def _get_cell_value(self, cell):
        if cell.ctype == XL_CELL_NUMBER:
            return int(cell.value)
        return cell.value

    def get_well_formed_cell_index(self, row_number, col_number):
        if col_number < 26:
            col_in_letters = chr(col_number + ord('A'))
        else:
            col_in_letters = chr((col_number - 1) / 26 + ord('A')) + chr(col_number % 26 + ord('A'))
        return '%s%s' % (col_in_letters, row_number + 1)

    def _is_empty(self, value):
        return str(value).strip() == ''

    def check_constraints(self, mappings):
        start_row_number = self.headers_row_number + 1
        cust_numbers = {}
        for field_name, column_number in mappings.items():
            model_field = models.Site._meta.get_field(field_name)
            for row_number in xrange(start_row_number, self.sheet.nrows):
                cell = self.sheet.cell(row_number, column_number)
                value = self._get_cell_value(cell)
                if field_name == self.CUST_NUMBER_FIELD_NAME:
                    if value in cust_numbers:
                        raise IntegrityError(Messages.Site.duplicate_cust_numbers % (self.get_well_formed_cell_index(cust_numbers[value][0], cust_numbers[value][1]), self.get_well_formed_cell_index(row_number, column_number)))
                    cust_numbers[value] = (row_number, column_number)
                if field_name in self.FOREIGN_KEY_FIELDS:
                    foreign_key_model = model_field.rel.to
                    available_values = foreign_key_model.objects.values_list('pk', flat=True).order_by('pk')
                    if not self._is_empty(value) and value not in available_values:
                        raise IntegrityError(Messages.Site.foreign_key_error % (self.get_well_formed_cell_index(row_number, column_number), ', '.join(map(str, available_values)), value))
                if self._is_empty(value) and (not model_field.null and model_field.default == NOT_PROVIDED):
                    raise IntegrityError(Messages.Site.required_value_is_empty % self.get_well_formed_cell_index(row_number, column_number))

    def parse_and_save(self, mappings, pws_pk):
        start_row_number = self.headers_row_number + 1
        new_sites = []
        counter = 0
        for row_number in xrange(start_row_number, self.sheet.nrows):
            cust_number_column_number = mappings['cust_number']
            cust_number_cell = self.sheet.cell(row_number, cust_number_column_number)
            cust_number = self._get_cell_value(cust_number_cell)
            try:
                site = models.Site.objects.get(pws__pk=pws_pk, cust_number=cust_number)
            except MultipleObjectsReturned:
                site = models.Site.objects.filter(pws__pk=pws_pk, cust_number=cust_number).first()
            except models.Site.DoesNotExist:
                site = models.Site()
                setattr(site, self.FOREIGN_KEY_PATTERN % self.PWS_FIELD_NAME, pws_pk)
            for field_name, column_number in mappings.items():
                cell = self.sheet.cell(row_number, column_number)
                value = self._get_cell_value(cell)
                if field_name in self.FOREIGN_KEY_FIELDS:
                    field_name = self.FOREIGN_KEY_PATTERN % field_name
                if field_name in self.DATE_FIELDS:
                    if not self._is_empty(value):
                        try:
                            value = datetime.strptime(str(value), self.DATE_FORMAT)
                        except ValueError:
                            raise DateFormatError(Messages.Site.incorrect_date_format % (self.get_well_formed_cell_index(row_number, column_number), self.DATE_FORMAT))
                    else:
                        value = None
                setattr(site, field_name, value)
            if site.pk:
                site.save()
            else:
                new_sites.append(site)
                counter += 1
                if counter == 1000:
                    models.Site.objects.bulk_create(new_sites)
                    counter = 0
                    new_sites = []
        models.Site.objects.bulk_create(new_sites)