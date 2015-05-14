import json
from optparse import make_option
from django.core.management import BaseCommand

from webapp.utils.excel_parser import ExcelParser


class Command(BaseCommand):
    help = 'Parses Excel file'

    option_list = BaseCommand.option_list + (
        make_option('--filename', help='Path to Excel file relative to MEDIA_ROOT'),
        make_option('--pws_pk', help='PWS\'s PK'),
        make_option('--mappings', help='Mappings between Excel fields and Site Model fields'),
    )

    def handle(self, *args, **options):
        filename = options['filename']
        pws_pk = int(options['pws_pk'])
        mappings = json.loads(options['mappings'])

        excel_parser = ExcelParser(filename)
        excel_parser.parse_and_save(mappings, pws_pk)