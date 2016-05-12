import json
from django.core.files.base import File
from datetime import datetime
import subprocess
import os
from bulk_update.helper import bulk_update
from django.conf import settings
import xlrd
import xlwt
from xlrd.biffh import XL_CELL_NUMBER, XL_CELL_TEXT

from main.parameters import SITE_STATUS
from webapp import models
from webapp.utils.excel_parser import ALPHABET_LENGTH, FOREIGN_KEY_PATTERN, FOREIGN_KEY_FIELDS, DATE_FIELDS, \
    DEFAULT_PROGRESS_UPDATE_STEP, FINISHED, DEFAULT_BULK_SIZE, RequiredValueIsEmptyError, \
    ForeignKeyError, DateFormatError, ExcelValidationError, NUMERIC_FIELDS, NumericValueError, \
    SPECIAL_FOREIGN_KEY_FIELDS
from webapp.utils.excel_parser.value_checkers import ValueCheckerFactory


class ExcelDocument(object):
    filename = None
    book = None
    sheet = None
    headers = []
    headers_row_number = None
    header_style = None

    def open_for_read(self):
        if not self.sheet:
            self.book = xlrd.open_workbook(self.filename)
            self.sheet = self.book.sheet_by_index(0)

    def open_for_write(self):
        if not self.sheet:
            self.book = xlwt.Workbook()
            self.sheet = self.book.add_sheet("Duplicates")
            self.header_style = xlwt.easyxf("font: bold on")

    def write_header(self, column, header):
        self.sheet.write(self.headers_row_number, column, header, self.header_style)

    def write_value(self, row, column, value):
        self.sheet.write(row, column, value)

    def write_to_file(self):
        self.book.save(self.filename)

    def parse_headers(self):
        self.open_for_read()
        if not self.headers:
            for column_number in xrange(self.sheet.ncols):
                cell = self.sheet.cell(self.headers_row_number, column_number)
                value = self.get_cell_value(cell)
                if value:
                    self.headers.append((column_number, value))
        return self.headers

    def get_cell_value(self, cell):
        if cell.ctype == XL_CELL_NUMBER:
            return int(cell.value)
        if cell.ctype == XL_CELL_TEXT:
            return cell.value.strip()
        return cell.value

    def get_cell(self, row, column):
        return self.sheet.cell(row, column)

    def get_first_n_rows(self, rows_count):
        self.open_for_read()
        example_rows = []
        start_row_number = self.headers_row_number + 1
        if rows_count + start_row_number > self.sheet.nrows:
            rows_count = self.sheet.nrows - start_row_number
        for row_number in xrange(start_row_number, start_row_number + rows_count):
            row = []
            for column_number, field_name in self.headers:
                cell = self.sheet.cell(row_number, column_number)
                row.append(self.get_cell_value(cell))
            example_rows.append(row)
        return example_rows

    def get_cell_value_by_coords(self, row, column):
        cell = self.get_cell(row, column)
        return self.get_cell_value(cell)

    @property
    def num_rows(self):
        if not self.sheet:
            self.open_for_read()
        return self.sheet.nrows


class ConstraintChecker(object):
    mappings = None
    date_format = None
    excel_document = None

    def __init__(self):
        self.required_value_errors = []
        self.date_format_errors = []
        self.foreign_key_errors = []
        self.numeric_value_errors = []

    def execute(self):
        start_row_number = self.excel_document.headers_row_number + 1
        for field_name, column_number in self.mappings.items():
            checker = ValueCheckerFactory.get_checker(field_name, date_format=self.date_format)
            for row_number in xrange(start_row_number, self.excel_document.num_rows):
                value = self.excel_document.get_cell_value_by_coords(row_number, column_number)
                try:
                    checker.check(value, self.prettify_cell_index(row_number, column_number))
                except RequiredValueIsEmptyError as e:
                    self.required_value_errors.append(str(e))
                except DateFormatError as e:
                    self.date_format_errors.append(str(e))
                except ForeignKeyError as e:
                    self.foreign_key_errors.append(str(e))
                except NumericValueError as e:
                    self.numeric_value_errors.append(str(e))

        if self.required_value_errors or \
                self.date_format_errors or \
                self.foreign_key_errors or \
                self.numeric_value_errors:
            raise ExcelValidationError(self.required_value_errors, self.date_format_errors,
                                       self.foreign_key_errors, self.numeric_value_errors)

    def prettify_cell_index(self, row_number, col_number):
        if col_number < ALPHABET_LENGTH:
            col_in_letters = chr(col_number + ord('A'))
        else:
            col_in_letters = chr((col_number - 1) / ALPHABET_LENGTH + ord('A')) + chr(col_number % ALPHABET_LENGTH + ord('A'))
        return '%s%s' % (col_in_letters, row_number + 1)


class BackgroundExcelParserRunner(object):
    mappings = None
    import_log_pk = None
    date_format = None
    filename = None
    update_only = None

    def execute(self):
        filename_option = '--filename="%s"' % self.filename
        json_mappings = json.dumps(json.dumps(self.mappings, separators=(',', ':')))
        mappings_option = '--mappings="%s"' % json_mappings
        import_log_option = '--import_log_pk="%d"' % self.import_log_pk
        date_format_option = '--date_format="%s"' % self.date_format
        update_only_option = '--update_only="%s"' % int(self.update_only)
        command = ' '.join((
            settings.PYTHON_EXECUTABLE,
            settings.MANAGE_PY,
            'parse_excel',
            filename_option,
            mappings_option,
            import_log_option,
            date_format_option,
            update_only_option
        ))
        subprocess.Popen(command, shell=True)


class ExcelParser(object):
    excel_document = None
    duplicate_account_rows = []

    def __init__(self, filename, headers_row_number=0):
        self.excel_document = ExcelDocument()
        self.excel_document.filename = filename
        self.excel_document.headers_row_number = headers_row_number

    def get_headers_as_choices(self):
        return self.excel_document.parse_headers()

    def get_example_rows(self, rows_count):
        return self.excel_document.get_first_n_rows(rows_count)

    def check_constraints(self, mappings, date_format):
        constraint_checker = ConstraintChecker()
        constraint_checker.excel_document = self.excel_document
        constraint_checker.mappings = mappings
        constraint_checker.date_format = date_format
        constraint_checker.execute()

    def find_duplicates(self, mappings):
        start_row_number = self.excel_document.headers_row_number + 1
        cust_account_column_number = mappings.get('cust_number')
        service_address_column_number = mappings.get('address1')
        street_number_column_number = mappings.get('street_number')
        columns_to_check = (cust_account_column_number, service_address_column_number, street_number_column_number)
        columns_to_check_count = len(columns_to_check)
        for row_number_1 in xrange(start_row_number, self.excel_document.num_rows-1):
            if row_number_1 not in self.duplicate_account_rows:
                is_duplicate = False
                for row_number_2 in xrange(row_number_1+1, self.excel_document.num_rows):
                    equal_columns = 0
                    for column in columns_to_check:
                        val1 = self.excel_document.get_cell_value_by_coords(row_number_1, column)
                        val2 = self.excel_document.get_cell_value_by_coords(row_number_2, column)
                        if val1 == val2:
                            equal_columns += 1
                    if equal_columns == columns_to_check_count:
                        self.duplicate_account_rows.append(row_number_2)
                        is_duplicate = True
                if is_duplicate:
                    self.duplicate_account_rows.append(row_number_1)

    def export_duplicates(self, mappings, import_log_pk):
        export_document = ExcelDocument()
        export_document.filename = os.path.join(
            '/tmp',
            'duplicate_' + os.path.basename(self.excel_document.filename)
        )
        export_document.headers_row_number = 0
        export_document.open_for_write()
        for column_number in xrange(0, self.excel_document.sheet.ncols):
            header = self.excel_document.get_cell_value_by_coords(self.excel_document.headers_row_number, column_number)
            export_document.write_header(column_number, header)
        current_row = 1
        for row_number in self.duplicate_account_rows:
            for column_number in xrange(0, self.excel_document.sheet.ncols):
                value = self.excel_document.get_cell_value_by_coords(row_number, column_number)
                export_document.write_value(current_row, column_number, value)
            current_row += 1
        export_document.write_to_file()
        import_log = models.ImportLog.objects.get(pk=import_log_pk)
        f = File(file(export_document.filename))
        import_log.duplicates_file = f
        import_log.duplicates_count = len(self.duplicate_account_rows)
        import_log.save()

    def parse_and_save(self, mappings, import_log_pk, date_format, update_only=False):
        self.find_duplicates(mappings)
        if len(self.duplicate_account_rows) > 0:
            self.export_duplicates(mappings, import_log_pk)

        import_log = models.ImportLog.objects.get(pk=import_log_pk)

        deactivated_sites_watcher = DeactivatedSitesWatcher(import_log.pws)
        updated_sites_watcher = UpdatedSitesWatcher()
        added_sites_watcher = AddedSitesWatcher()

        total_rows_with_data = self.excel_document.num_rows
        progress_watcher = ProgressWatcher(import_log, total_rows_with_data)

        start_row_number = self.excel_document.headers_row_number + 1

        active_status = models.SiteStatus.objects.get(site_status__iexact=SITE_STATUS.ACTIVE)
        inactive_status = models.SiteStatus.objects.get(site_status__iexact=SITE_STATUS.INACTIVE)

        cust_account_column_number = mappings.pop('cust_number')
        service_address_column_number = mappings.pop('address1')
        street_number_column_number = mappings.pop('street_number')

        for row_number in xrange(start_row_number, self.excel_document.num_rows):
            if row_number not in self.duplicate_account_rows:
                cust_number = self.excel_document.get_cell_value_by_coords(row_number, cust_account_column_number)
                service_address = self.excel_document.get_cell_value_by_coords(row_number, service_address_column_number)
                street_number = self.excel_document.get_cell_value_by_coords(row_number, street_number_column_number)
                try:
                    site = models.Site.objects.get(pws=import_log.pws, cust_number=cust_number,
                                                   address1=service_address, street_number=street_number)
                    deactivated_sites_watcher.remove(site)
                except models.Site.DoesNotExist:
                    site = models.Site()
                    site.pws = import_log.pws
                    site.cust_number = cust_number
                    site.street_number = street_number
                    site.address1 = service_address
                site.status = active_status
                for field_name, column_number in mappings.items():
                    value = self.excel_document.get_cell_value_by_coords(row_number, column_number)
                    if field_name in FOREIGN_KEY_FIELDS:
                        field_name = FOREIGN_KEY_PATTERN % field_name
                    if field_name in SPECIAL_FOREIGN_KEY_FIELDS:
                        search_expression = {SPECIAL_FOREIGN_KEY_FIELDS[field_name]['field']: value}
                        foreign_key_value = SPECIAL_FOREIGN_KEY_FIELDS[field_name]['model'].objects.get(
                            **search_expression
                        )
                        value = foreign_key_value
                    if field_name in DATE_FIELDS:
                        if value:
                            value = datetime.strptime(str(value), date_format)
                        else:
                            value = None
                    if field_name in NUMERIC_FIELDS:
                        if value:
                            value = float(value)
                        else:
                            value = 0
                    setattr(site, field_name, value)
                if site.pk:
                    updated_sites_watcher.add(site)
                else:
                    added_sites_watcher.add(site)
                progress_watcher.increment_processed_rows()
            else:
                cust_number = self.excel_document.get_cell_value_by_coords(row_number, cust_account_column_number)
                service_address = self.excel_document.get_cell_value_by_coords(row_number, service_address_column_number)
                street_number = self.excel_document.get_cell_value_by_coords(row_number, street_number_column_number)
                try:
                    site = models.Site.objects.get(pws=import_log.pws, cust_number=cust_number,
                                                   address1=service_address, street_number=street_number)
                    deactivated_sites_watcher.remove(site)
                except models.Site.DoesNotExist:
                    pass

        updated_sites_watcher.perform_bulk_update()
        added_sites_watcher.perform_bulk_create()

        if not update_only:
            deactivated_sites = deactivated_sites_watcher.get_deactivated_sites()
            deactivated_sites.update(status=inactive_status)
        else:
            deactivated_sites = models.Site.objects.none()
        import_log.deactivated_sites = deactivated_sites

        updated_sites = updated_sites_watcher.get_updated_sites()
        import_log.updated_sites = updated_sites

        added_sites = added_sites_watcher.get_added_sites()
        import_log.added_sites = added_sites

        import_log.save()
        progress_watcher.set_as_finished()


class ProgressWatcher(object):
    def __init__(self, import_log, total_rows, update_step=DEFAULT_PROGRESS_UPDATE_STEP):
        self.import_log = import_log
        self.total_rows = total_rows
        self.update_step = update_step
        self.processed_rows = 0

    def increment_processed_rows(self):
        self.processed_rows += 1
        if self.processed_rows % self.update_step == 0:
            self.import_log.progress = int(float(FINISHED) * self.processed_rows / self.total_rows)
            self.import_log.save()

    def set_as_finished(self):
        self.import_log.progress = FINISHED
        self.import_log.save()


class DeactivatedSitesWatcher(object):
    def __init__(self, pws):
        self.deactivated_site_pks = list(models.Site.objects.filter(pws=pws).values_list('pk', flat=True))

    def remove(self, site):
        try:
            self.deactivated_site_pks.remove(site.pk)
        except ValueError:
            pass

    def get_deactivated_sites(self):
        return models.Site.objects.filter(pk__in=self.deactivated_site_pks)


class UpdatedSitesWatcher(object):
    def __init__(self, batch_size=DEFAULT_BULK_SIZE):
        self.updated_sites = []
        self.updated_site_pks = []
        self.batch_size = batch_size

    def add(self, site, perform_bulk_update=True):
        self.updated_sites.append(site)
        self.updated_site_pks.append(site.pk)
        if perform_bulk_update and len(self.updated_sites) >= self.batch_size:
            self.perform_bulk_update()

    def perform_bulk_update(self):
        if self.updated_sites:
            bulk_update(self.updated_sites)
            self.updated_sites = []

    def get_updated_sites(self):
        return models.Site.objects.filter(pk__in=self.updated_site_pks)


class AddedSitesWatcher(object):
    def __init__(self, batch_size=DEFAULT_BULK_SIZE):
        self.added_sites = []
        self.added_site_pks = []
        self.batch_size = batch_size

    def add(self, site, perform_bulk_update=True):
        self.added_sites.append(site)
        if perform_bulk_update and len(self.added_sites) >= self.batch_size:
            self.perform_bulk_create()

    def perform_bulk_create(self):
        existing_site_pks = list(models.Site.objects.values_list('pk', flat=True))
        models.Site.objects.bulk_create(self.added_sites)
        self.added_sites = []
        added_sites_pks = list(models.Site.objects.exclude(pk__in=existing_site_pks).values_list('pk', flat=True))
        self.added_site_pks.extend(added_sites_pks)

    def get_added_sites(self):
        return models.Site.objects.filter(pk__in=self.added_site_pks)
