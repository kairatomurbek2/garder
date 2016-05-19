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


class ExcelParser(object):
    duplicate_account_rows = []

    def __init__(self, filename, headers_row_number=0):
        self.import_document = ExcelDocument(filename, EXCEL_MODE_READ, headers_row_number)
        export_doc_filename = os.path.join(
            '/tmp',
            'duplicate_' + os.path.basename(self.import_document.filename)
        )
        self.export_document = ExcelDocument(export_doc_filename, EXCEL_MODE_WRITE)

    def get_headers_as_choices(self):
        return self.import_document.read_headers()

    def get_example_rows(self, rows_count):
        return self.import_document.read_n_headered_rows(rows_count)

    def check_constraints(self, mappings, date_format):
        constraint_checker = ConstraintChecker()
        constraint_checker.excel_document = self.import_document
        constraint_checker.mappings = mappings
        constraint_checker.date_format = date_format
        constraint_checker.execute()

    def _find_duplicates(self, mappings):
        start_row_number = self.import_document.header_row + 1
        columns_to_check = (mappings.get('cust_number'), mappings.get('meter_number'),
                            mappings.get('address1'), mappings.get('street_number'))
        columns_to_check_count = len(columns_to_check)
        for row_number_1 in xrange(start_row_number, self.import_document.row_count-1):
            if row_number_1 not in self.duplicate_account_rows:
                is_duplicate = False
                for row_number_2 in xrange(row_number_1+1, self.import_document.row_count):
                    equal_columns = 0
                    for column in columns_to_check:
                        val1 = self.import_document.read_cell(row_number_1, column)
                        val2 = self.import_document.read_cell(row_number_2, column)
                        if val1 == val2:
                            equal_columns += 1
                    if equal_columns == columns_to_check_count:
                        self.duplicate_account_rows.append(row_number_2)
                        is_duplicate = True
                if is_duplicate:
                    self.duplicate_account_rows.append(row_number_1)

    def _write_export_headers(self):
        if self.export_document.current_row < 0:
            self.export_document.set_write_style(EXCEL_WRITE_STYLE_BOLD)
            self.export_document.write_next_row(*self.import_document.read_row(self.import_document.header_row))
            self.export_document.set_write_style(EXCEL_WRITE_STYLE_NORMAL)

    def _export_rows_from_file(self, row_numbers):
        if len(row_numbers) > 0:
            self._write_export_headers()
            for row_number in row_numbers:
                self.export_document.write_next_row(*self.import_document.read_row(row_number))

    def _export_existing_sites(self, site_pks):
        if len(site_pks) > 0:
            self._write_export_headers()
            row = self.export_document.current_row + 1
            original_mappings_items = self.original_mappings.items()
            self.export_document.set_write_style(EXCEL_WRITE_STYLE_ITALIC)
            for site_pk in site_pks:
                site = models.Site.objects.get(pk=site_pk)
                last_col = 0
                for field_name, column in original_mappings_items:
                    value = self._get_site_field_value_for_export(getattr(site, field_name, ""), field_name)
                    self.export_document.write_cell(row, column, value)
                    if column > last_col:
                        last_col = column
                self.export_document.write_cell(row, last_col + 1, str(site.status))
                row += 1
            self.export_document.set_write_style(EXCEL_WRITE_STYLE_NORMAL)

    def _get_site_field_value_for_export(self, originalValue, field_name):
        if field_name in DATE_FIELDS:
            if originalValue:
                return originalValue.strftime(self.date_format)
        return str(originalValue)

    def _attach_export_document(self):
        if self.export_document.current_row < 0:
            self.export_document.close(save=False)
        else:
            self.export_document.close()
            f = File(file(self.export_document.filename))
            self.import_log.duplicates_file = f
            self.import_log.duplicates_count = len(self.duplicate_account_rows) + len(self.ambiguous_rows)
            self.import_log.save()

    def parse_and_save(self, mappings, import_log_pk, date_format, update_only=False):
        self._find_duplicates(mappings)
        self._export_rows_from_file(self.duplicate_account_rows)
        self._init_import_parameters(mappings, import_log_pk, date_format)
        start_row_number = self.import_document.header_row + 1
        for row_number in xrange(start_row_number, self.import_document.row_count):
            self._setup_unique_key_fields(row_number)
            if row_number in self.duplicate_account_rows:
                self._remove_duplicate_from_deactivated_watcher()
                continue
            try:
                site = self._get_existing_site()
                self.deactivated_sites_watcher.remove(site)
                self.updated_site_pks.append(site.pk)
            except models.Site.DoesNotExist:
                if self.cust_number in self.ambiguous_accounts:
                    self.ambiguous_rows.append(row_number)
                    continue
                sites = models.Site.objects.filter(pws=self.import_log.pws, cust_number=self.cust_number)
                if sites.count() > 0:
                    self._process_ambiguous_sites(sites)
                    self.ambiguous_accounts.append(self.cust_number)
                    self.ambiguous_rows.append(row_number)
                    continue
                site = self._get_new_site()
            self._update_site_from_row(site, row_number)
            site.status = self.active_status
            self._update_watchers(site)
        self._export_rows_from_file(self.ambiguous_rows)
        ambiguous_site_pks = list(set(self.ambiguous_site_pks) - set(self.updated_site_pks))
        self._export_existing_sites(ambiguous_site_pks)
        self._attach_export_document()
        self._finish_import(update_only)

    def _update_watchers(self, site):
        if site.pk:
            self.updated_sites_watcher.add(site)
        else:
            self.added_sites_watcher.add(site)
        self.progress_watcher.increment_processed_rows()

    def _get_existing_site(self):
        return models.Site.objects.get(pws=self.import_log.pws, cust_number=self.cust_number,
                                       meter_number=self.meter_number, address1=self.service_address,
                                       street_number=self.street_number)

    def _get_new_site(self):
        site = models.Site()
        site.pws = self.import_log.pws
        site.cust_number = self.cust_number
        return site

    def _remove_duplicate_from_deactivated_watcher(self):
        try:
            site = models.Site.objects.get(pws=self.import_log.pws, cust_number=self.cust_number,
                                           meter_number=self.meter_number, address1=self.service_address,
                                           street_number=self.street_number)
            self.deactivated_sites_watcher.remove(site)
        except models.Site.DoesNotExist:
            pass

    def _process_ambiguous_sites(self, sites):
        for site in sites:
            self.deactivated_sites_watcher.remove(site)
            self.ambiguous_site_pks.append(site.pk)

    def _setup_unique_key_fields(self, row_number):
        self.cust_number = self._get_cell_value_for_mapped_column(row_number, 'cust_number')
        self.meter_number = self._get_cell_value_for_mapped_column(row_number, 'meter_number')
        self.service_address = self._get_cell_value_for_mapped_column(row_number, 'address1')
        self.street_number = self._get_cell_value_for_mapped_column(row_number, 'street_number')

    def _get_cell_value_for_mapped_column(self, row, column_name):
        return self.import_document.read_cell(row, self.original_mappings.get(column_name))

    def _init_import_parameters(self, mappings, import_log_pk, date_format):
        self.date_format = date_format
        self.import_log = models.ImportLog.objects.get(pk=import_log_pk)
        self.mappings = mappings
        self.original_mappings = dict(mappings)
        self.mappings.pop('cust_number')
        self.deactivated_sites_watcher = DeactivatedSitesWatcher(self.import_log.pws)
        self.updated_sites_watcher = UpdatedSitesWatcher()
        self.added_sites_watcher = AddedSitesWatcher()
        total_rows_with_data = self.import_document.row_count - self.import_document.header_row
        self.progress_watcher = ProgressWatcher(self.import_log, total_rows_with_data)
        self.active_status = models.SiteStatus.objects.get(site_status__iexact=SITE_STATUS.ACTIVE)
        self.inactive_status = models.SiteStatus.objects.get(site_status__iexact=SITE_STATUS.INACTIVE)
        self.ambiguous_accounts = []  # from file, inner usage
        self.updated_site_pks = []  # from database, inner usage
        self.ambiguous_site_pks = []  # from database, for export
        self.ambiguous_rows = []  # from file, for export

    def _update_site_from_row(self, site, row_number):
        for field_name, column_number in self.mappings.items():
            value = self.import_document.read_cell(row_number, column_number)
            if field_name in FOREIGN_KEY_FIELDS:
                field_name = FOREIGN_KEY_PATTERN % field_name
            elif field_name in SPECIAL_FOREIGN_KEY_FIELDS:
                search_expression = {SPECIAL_FOREIGN_KEY_FIELDS[field_name]['field']: value}
                foreign_key_value = SPECIAL_FOREIGN_KEY_FIELDS[field_name]['model'].objects.get(
                    **search_expression
                )
                value = foreign_key_value
            elif field_name in DATE_FIELDS:
                if value:
                    value = datetime.strptime(str(value), self.date_format)
                else:
                    value = None
            elif field_name in NUMERIC_FIELDS:
                if value:
                    value = float(value)
                else:
                    value = 0
            setattr(site, field_name, value)

    def _finish_import(self, update_only):
        self.updated_sites_watcher.perform_bulk_update()
        self.added_sites_watcher.perform_bulk_create()
        updated_sites = self.updated_sites_watcher.get_updated_sites()
        added_sites = self.added_sites_watcher.get_added_sites()
        if not update_only:
            deactivated_sites = self.deactivated_sites_watcher.get_deactivated_sites()
            deactivated_sites.update(status=self.inactive_status)
        else:
            deactivated_sites = models.Site.objects.none()
        self.import_log.deactivated_sites = deactivated_sites
        self.import_log.updated_sites = updated_sites
        self.import_log.added_sites = added_sites
        self.import_log.save()
        self.progress_watcher.set_as_finished()


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
        active_status = models.SiteStatus.objects.get(site_status__iexact=SITE_STATUS.ACTIVE)
        self.deactivated_site_pks = list(models.Site.objects.filter(
            pws=pws,
            status=active_status
        ).values_list('pk', flat=True))

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
