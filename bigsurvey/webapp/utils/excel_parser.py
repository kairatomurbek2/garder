import json
from datetime import datetime
import subprocess

from bulk_update.helper import bulk_update
from django.conf import settings
from django.db import IntegrityError
from django.db.models import NOT_PROVIDED, Q
import xlrd
from xlrd.biffh import XL_CELL_NUMBER

from main.parameters import Messages

from webapp import models


ALPHABET_LENGTH = 26
FINISHED = 100
DEFAULT_BULK_SIZE = 1000
DEFAULT_PROGRESS_UPDATE_STEP = 1000


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
        self.filename = filename
        self.book = None
        self.sheet = None
        self.headers = []
        self.headers_row_number = headers_row_number

    def open(self):
        if not self.sheet:
            self.book = xlrd.open_workbook(self.filename)
            self.sheet = self.book.sheet_by_index(0)

    def _parse_headers(self):
        self.open()
        for column_number in xrange(self.sheet.ncols):
            cell = self.sheet.cell(self.headers_row_number, column_number)
            value = self._get_cell_value(cell)
            if not self._is_empty(value):
                self.headers.append((column_number, value))

    def get_headers_as_choices(self):
        if not self.headers:
            self._parse_headers()
        return self.headers

    def get_example_rows(self, rows_count):
        self.open()
        example_rows = []
        start_row_number = self.headers_row_number + 1
        if rows_count + start_row_number > self.sheet.nrows:
            rows_count = self.sheet.nrows - start_row_number
        for row_number in xrange(start_row_number, start_row_number + rows_count):
            row = []
            for column_number, field_name in self.headers:
                cell = self.sheet.cell(row_number, column_number)
                row.append(self._get_cell_value(cell))
            example_rows.append(row)
        return example_rows

    def _get_cell_value(self, cell):
        if cell.ctype == XL_CELL_NUMBER:
            return int(cell.value)
        return cell.value

    def prettify_cell_index(self, row_number, col_number):
        if col_number < ALPHABET_LENGTH:
            col_in_letters = chr(col_number + ord('A'))
        else:
            col_in_letters = chr((col_number - 1) / ALPHABET_LENGTH + ord('A')) + chr(col_number % ALPHABET_LENGTH + ord('A'))
        return '%s%s' % (col_in_letters, row_number + 1)

    def _is_empty(self, value):
        return str(value).strip() == ''

    def check_constraints(self, mappings):
        self.open()
        start_row_number = self.headers_row_number + 1
        cust_numbers = {}
        for field_name, column_number in mappings.items():
            model_field = models.Site._meta.get_field(field_name)
            for row_number in xrange(start_row_number, self.sheet.nrows):
                cell = self.sheet.cell(row_number, column_number)
                value = self._get_cell_value(cell)
                if field_name == self.CUST_NUMBER_FIELD_NAME:
                    if value in cust_numbers:
                        raise IntegrityError(
                            Messages.Import.duplicate_cust_numbers % (self.prettify_cell_index(cust_numbers[value][0], cust_numbers[value][1]), self.prettify_cell_index(row_number, column_number)))
                    cust_numbers[value] = (row_number, column_number)
                if field_name in self.DATE_FIELDS:
                    if not self._is_empty(value):
                        try:
                            datetime.strptime(str(value), self.DATE_FORMAT)
                        except ValueError:
                            raise DateFormatError(Messages.Import.incorrect_date_format % (self.prettify_cell_index(row_number, column_number), self.DATE_FORMAT))
                if field_name in self.FOREIGN_KEY_FIELDS:
                    foreign_key_model = model_field.rel.to
                    available_values = foreign_key_model.objects.values_list('pk', flat=True).order_by('pk')
                    if not self._is_empty(value) and value not in available_values:
                        raise IntegrityError(Messages.Import.foreign_key_error % (self.prettify_cell_index(row_number, column_number), ', '.join(map(str, available_values)), value))
                if self._is_empty(value) and (not model_field.null and model_field.default == NOT_PROVIDED):
                    raise IntegrityError(Messages.Import.required_value_is_empty % self.prettify_cell_index(row_number, column_number))

    def parse_and_save_in_background(self, mappings, pws_pk, import_progress_pk, user_pk):
        filename_option = '--filename=%s' % self.filename
        pws_option = '--pws_pk=%d' % pws_pk
        json_mappings = json.dumps(json.dumps(mappings, separators=(',', ':')))
        mappings_option = '--mappings=%s' % json_mappings
        import_progress_option = '--import_progress_pk=%d' % import_progress_pk
        user_option = '--user_pk=%d' % user_pk
        command = '%s %s %s %s %s %s %s %s' % (settings.PYTHON_EXECUTABLE, settings.MANAGE_PY, 'parse_excel', filename_option, pws_option, mappings_option, import_progress_option, user_option)
        subprocess.Popen(command, shell=True)

    def parse_and_save(self, mappings, pws_pk, import_progress_pk, user_pk):
        self.open()

        pws = models.PWS.objects.get(pk=pws_pk)
        import_progress = models.ImportProgress.objects.get(pk=import_progress_pk)
        import_log = models.ImportLog()
        import_log.pws = pws
        import_log.user = models.User.objects.get(pk=user_pk)
        import_log.save()

        deactivated_sites_watcher = DeactivatedSitesWatcher(pws)
        updated_sites_watcher = UpdatedSitesWatcher()
        added_sites_watcher = AddedSitesWatcher()

        total_rows = self.sheet.nrows - self.headers_row_number
        progress_watcher = ProgressWatcher(import_progress, total_rows)

        start_row_number = self.headers_row_number + 1

        active_status = models.SiteStatus.objects.get(site_status__iexact='Active')
        inactive_status = models.SiteStatus.objects.get(site_status__iexact='Inactive')

        cust_number_column_number = mappings.pop('cust_number')

        for row_number in xrange(start_row_number, self.sheet.nrows):
            cust_number_cell = self.sheet.cell(row_number, cust_number_column_number)
            cust_number = self._get_cell_value(cust_number_cell)
            try:
                site = models.Site.objects.get(pws=pws, cust_number=cust_number)
                deactivated_sites_watcher.remove(site)
            except models.Site.DoesNotExist:
                site = models.Site()
                site.pws = pws
                site.cust_number = cust_number
            site.status = active_status
            for field_name, column_number in mappings.items():
                cell = self.sheet.cell(row_number, column_number)
                value = self._get_cell_value(cell)
                if field_name in self.FOREIGN_KEY_FIELDS:
                    field_name = self.FOREIGN_KEY_PATTERN % field_name
                if field_name in self.DATE_FIELDS:
                    if not self._is_empty(value):
                        value = datetime.strptime(str(value), self.DATE_FORMAT)
                    else:
                        value = None
                setattr(site, field_name, value)
            if site.pk:
                updated_sites_watcher.add(site)
            else:
                added_sites_watcher.add(site)
            progress_watcher.increment_processed_rows()

        updated_sites_watcher.perform_bulk_update()
        added_sites_watcher.perform_bulk_create()

        deactivated_sites = deactivated_sites_watcher.get_deactivated_sites()
        deactivated_sites.update(status=inactive_status)
        import_log.deactivated_sites = deactivated_sites

        updated_sites = updated_sites_watcher.get_updated_sites()
        import_log.updated_sites = updated_sites

        added_sites = added_sites_watcher.get_added_sites()
        import_log.added_sites = added_sites

        import_log.save()

        import_progress.progress = FINISHED
        import_progress.save()


class ProgressWatcher(object):
    def __init__(self, import_progress, total_rows, update_step=DEFAULT_PROGRESS_UPDATE_STEP):
        self.import_progress = import_progress
        self.total_rows = total_rows
        self.update_step = update_step
        self.processed_rows = 0

    def increment_processed_rows(self):
        self.processed_rows += 1
        if self.processed_rows % self.update_step == 0:
            self.import_progress.progress = int(float(FINISHED) * self.processed_rows / self.total_rows)
            self.import_progress.save()


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