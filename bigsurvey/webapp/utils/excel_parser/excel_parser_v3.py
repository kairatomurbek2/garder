# -*- coding: utf-8 -*-

import json
from django.core.files.base import File
from datetime import datetime
import subprocess
import os
from bulk_update.helper import bulk_update
from django.conf import settings
from main.parameters import SITE_STATUS
from webapp import models
from webapp.utils.excel_parser import ALPHABET_LENGTH, FOREIGN_KEY_PATTERN, FOREIGN_KEY_FIELDS, DATE_FIELDS, \
    DEFAULT_PROGRESS_UPDATE_STEP, FINISHED, DEFAULT_BULK_SIZE, RequiredValueIsEmptyError, \
    ForeignKeyError, DateFormatError, ExcelValidationError, NUMERIC_FIELDS, NumericValueError, \
    SPECIAL_FOREIGN_KEY_FIELDS
from webapp.utils.excel_parser.value_checkers import ValueCheckerFactory
from .excel_document import ExcelDocument, EXCEL_MODE_READ, EXCEL_MODE_WRITE, \
    EXCEL_WRITE_STYLE_BOLD, EXCEL_WRITE_STYLE_NORMAL, EXCEL_WRITE_STYLE_ITALIC

# Отрефакторенный парсер
# Работает так же, как v2, по схеме из #361
# Отличается порядком работы и более структурированным кодом


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
        start_row_number = self.excel_document.header_row + 1
        for field_name, column_number in self.mappings.items():
            checker = ValueCheckerFactory.get_checker(field_name, date_format=self.date_format)
            for row_number in xrange(start_row_number, self.excel_document.row_count):
                value = self.excel_document.read_cell(row_number, column_number)
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

    def execute(self, debug=False):
        if debug:
            excel_parser = ExcelParser(os.path.join(settings.EXCEL_FILES_DIR, self.filename))
            excel_parser.parse_and_save(self.mappings, self.import_log_pk, self.date_format, self.update_only)
        else:
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


# more readable code than in original excel parser
# probably slower logic
class ExcelParser(object):
    def __init__(self, filename, headers_row_number=0):
        self._import_document = ExcelDocument(filename, EXCEL_MODE_READ, headers_row_number)
        export_doc_filename = os.path.join(
            '/tmp',
            'duplicate_' + os.path.basename(self._import_document.filename)
        )
        self._export_document = ExcelDocument(export_doc_filename, EXCEL_MODE_WRITE)

    def get_headers_as_choices(self):
        return self._import_document.read_headers()

    def get_example_rows(self, rows_count):
        return self._import_document.read_n_headered_rows(rows_count)

    def check_constraints(self, mappings, date_format):
        constraint_checker = ConstraintChecker()
        constraint_checker.excel_document = self._import_document
        constraint_checker.mappings = mappings
        constraint_checker.date_format = date_format
        constraint_checker.execute()

    def parse_and_save(self, mappings, import_log_pk, date_format, update_only=False):
        try:
            self._init_parameters(mappings, import_log_pk, date_format, update_only)
            self._exclude_duplicates()
            self._find_sites_to_update()
            self._find_sites_to_add()
            self._find_sites_to_deactivate()
            self._exclude_sites_left()
            self._export_excluded()
            self._submit_database_changes()
        except Exception as e:
            print e.message
            self._progress_watcher.set_as_finished()

    def _init_parameters(self, mappings, import_log_pk, date_format, update_only):
        self._mappings = mappings
        self._import_log = models.ImportLog.objects.get(pk=import_log_pk)
        self._date_format = date_format
        self._update_only = update_only
        self._duplicate_rows = []
        self._processed_site_pks = []
        self._added_watcher = AddedSitesWatcher()
        self._updated_watcher = UpdatedSitesWatcher()
        self._progress_watcher = ProgressWatcher(self._import_log, self._import_document.row_count)

    def _exclude_duplicates(self):
        fields_to_check = (self._mappings.get('cust_number'), self._mappings.get('meter_number'),
                           self._mappings.get('address1'), self._mappings.get('street_number'))
        max_equal_fields = len(fields_to_check)
        for first_row in xrange(self._import_document.header_row + 1, self._import_document.row_count-1):
            if first_row not in self._duplicate_rows:
                is_duplicate = False
                for second_row in xrange(first_row+1, self._import_document.row_count):
                    equal_fields = 0
                    for column in fields_to_check:
                        val1 = self._import_document.read_cell(first_row, column)
                        val2 = self._import_document.read_cell(second_row, column)
                        if val1 == val2:
                            equal_fields += 1
                    if equal_fields == max_equal_fields:
                        self._duplicate_rows.append(second_row)
                        is_duplicate = True
                if is_duplicate:
                    self._duplicate_rows.append(first_row)
        self._processed_rows = list(self._duplicate_rows)

    def _find_sites_to_update(self):
        cust_number_col = self._mappings.get('cust_number')
        meter_number_col = self._mappings.get('meter_number')
        street_address_col = self._mappings.get('address1')
        street_number_col = self._mappings.get('street_number')
        active_status = models.SiteStatus.objects.get(site_status__iexact=SITE_STATUS.ACTIVE)
        for row in xrange(self._import_document.header_row + 1, self._import_document.row_count):
            cust_number = self._import_document.read_cell(row, cust_number_col)
            meter_number = self._import_document.read_cell(row, meter_number_col)
            street_address = self._import_document.read_cell(row, street_address_col)
            street_number = self._import_document.read_cell(row, street_number_col)
            if row in self._processed_rows:
                continue
            try:
                site = models.Site.objects.get(pws=self._import_log.pws, cust_number=cust_number,
                                               meter_number=meter_number, address1=street_address,
                                               street_number=street_number)
                site.status = active_status
                self._update_site_from_row(site, row)
                self._updated_watcher.add(site)
                self._processed_site_pks.append(site.pk)
                self._processed_rows.append(row)
                self._progress_watcher.increment_processed_rows()
            except models.Site.DoesNotExist:
                pass

    def _update_site_from_row(self, site, row_number):
        for field_name, column_number in self._mappings.items():
            value = self._import_document.read_cell(row_number, column_number)
            if field_name in FOREIGN_KEY_FIELDS:
                field_name = FOREIGN_KEY_PATTERN % field_name
            elif field_name in SPECIAL_FOREIGN_KEY_FIELDS:
                search_expression = {SPECIAL_FOREIGN_KEY_FIELDS[field_name]['field']: value}
                foreign_key_value = SPECIAL_FOREIGN_KEY_FIELDS[field_name]['model'].objects.get(**search_expression)
                value = foreign_key_value
            elif field_name in DATE_FIELDS:
                value = None
                if value:
                    value = datetime.strptime(str(value), self._date_format)
            elif field_name in NUMERIC_FIELDS:
                value = 0
                if value:
                    value = float(value)
            else:
                value = str(value)
            setattr(site, field_name, value)

    def _find_sites_to_add(self):
        cust_number_col = self._mappings.get('cust_number')
        active_status = models.SiteStatus.objects.get(site_status__iexact=SITE_STATUS.ACTIVE)
        for row in xrange(self._import_document.header_row + 1, self._import_document.row_count):
            if row in self._processed_rows:
                continue
            cust_number = self._import_document.read_cell(row, cust_number_col)
            existing_sites = models.Site.objects.filter(
                pws=self._import_log.pws, cust_number=cust_number, status=active_status
            )
            if existing_sites.count() > 0:
                continue
            site = models.Site()
            site.pws = self._import_log.pws
            site.status = active_status
            self._update_site_from_row(site, row)
            self._added_watcher.add(site)
            self._processed_rows.append(row)
            self._progress_watcher.increment_processed_rows()

    def _find_sites_to_deactivate(self):
        cust_number_col = self._mappings.get('cust_number')
        imported_accounts = self._import_document.read_column(cust_number_col)
        active_status = models.SiteStatus.objects.get(site_status__iexact=SITE_STATUS.ACTIVE)
        unimported_sites = models.Site.objects\
            .filter(pws=self._import_log.pws)\
            .exclude(cust_number__in=imported_accounts)
        self._sites_to_deactivate = unimported_sites.filter(status=active_status)
        self._processed_site_pks.extend(unimported_sites.values_list('pk', flat=True))

    def _exclude_sites_left(self):
        self._ambiguous_sites = models.Site.objects\
            .filter(pws=self._import_log.pws)\
            .exclude(pk__in=self._processed_site_pks)
        self._ambiguous_rows = list(
            set(range(self._import_document.header_row+1, self._import_document.row_count)) - set(self._processed_rows)
        )

    def _export_excluded(self):
        self._export_rows_from_imported_file(self._duplicate_rows)
        self._export_rows_from_imported_file(self._ambiguous_rows)
        self._export_existing_sites(self._ambiguous_sites)
        self._attach_export_document()

    def _write_export_headers(self):
        if self._export_document.current_row < 0:
            self._export_document.set_write_style(EXCEL_WRITE_STYLE_BOLD)
            self._export_document.write_next_row(*self._import_document.read_row(self._import_document.header_row))
            self._export_document.set_write_style(EXCEL_WRITE_STYLE_NORMAL)

    def _export_rows_from_imported_file(self, rows):
        if len(rows) > 0:
            self._write_export_headers()
            for row in rows:
                self._export_document.write_next_row(*self._import_document.read_row(row))

    def _export_existing_sites(self, sites):
        if len(sites) > 0:
            self._write_export_headers()
            row = self._export_document.current_row + 1
            original_mappings_items = self._mappings.items()
            self._export_document.set_write_style(EXCEL_WRITE_STYLE_ITALIC)
            for site in sites:
                last_col = 0
                for field_name, column in original_mappings_items:
                    value = self._get_site_field_value_for_export(getattr(site, field_name, ""), field_name)
                    self._export_document.write_cell(row, column, value)
                    if column > last_col:
                        last_col = column
                self._export_document.write_cell(row, last_col + 1, str(site.status))
                row += 1
            self._export_document.set_write_style(EXCEL_WRITE_STYLE_NORMAL)

    def _get_site_field_value_for_export(self, originalValue, field_name):
        if not originalValue:
            return ""
        if field_name in DATE_FIELDS:
            return originalValue.strftime(self._date_format)
        return str(originalValue)

    def _attach_export_document(self):
        if self._export_document.current_row < 0:
            self._export_document.close(save=False)
        else:
            self._export_document.close()
            f = File(file(self._export_document.filename))
            self._import_log.duplicates_file = f
            self._import_log.duplicates_count = len(self._duplicate_rows) + len(self._ambiguous_rows)
            self._import_log.save()

    def _submit_database_changes(self):
        self._added_watcher.perform_bulk_create()
        self._updated_watcher.perform_bulk_update()
        if self._update_only:
            self._import_log.deactivated_sites = models.Site.objects.none()
        else:
            inactive_status = models.SiteStatus.objects.get(site_status__iexact=SITE_STATUS.INACTIVE)
            self._import_log.deactivated_sites = self._sites_to_deactivate.all()
            self._sites_to_deactivate.update(status=inactive_status)
        self._import_log.added_sites = self._added_watcher.get_added_sites()
        self._import_log.updated_sites = self._updated_watcher.get_updated_sites()
        self._import_log.save()
        self._progress_watcher.set_as_finished()


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
