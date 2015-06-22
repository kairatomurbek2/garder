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
        make_option('--pws_pk', help='PWS\'s PK'),
        make_option('--mappings', help='Mappings between Excel fields and Site Model fields'),
        make_option('--import_progress_pk', help='Import Progress\'s PK'),
        make_option('--user_pk', help='User\'s PK'),
    )

    def handle(self, *args, **options):
        filename = options['filename']
        pws_pk = int(options['pws_pk'])
        mappings = json.loads(options['mappings'])
        import_progress_pk = int(options['import_progress_pk'])
        user_pk = int(options['user_pk'])

        excel_parser = ExcelParser(os.path.join(settings.EXCEL_FILES_DIR, filename))
        excel_parser.parse_and_save(mappings, pws_pk, import_progress_pk, user_pk)