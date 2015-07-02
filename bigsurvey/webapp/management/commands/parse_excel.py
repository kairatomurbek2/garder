import json
from optparse import make_option
import os

from django.conf import settings
from django.core.management import BaseCommand

from webapp.utils.excel_parser import ExcelParser


class Command(BaseCommand):
    help = 'Parses Excel file'

    option_list = BaseCommand.option_list + (
        make_option('--filename', help='Path to Excel file'),
        make_option('--mappings', help='Mappings between Excel fields and Site Model fields'),
        make_option('--import_log_pk', help='Import Log\'s PK'),
        make_option('--date_format', help='Date Format'),
    )

    def handle(self, *args, **options):
        filename = options['filename']
        mappings = json.loads(options['mappings'])
        import_log_pk = int(options['import_log_pk'])
        date_format = options['date_format']

        excel_parser = ExcelParser(os.path.join(settings.EXCEL_FILES_DIR, filename))
        excel_parser.parse_and_save(mappings, import_log_pk, date_format)