from optparse import make_option
from django.core.management import BaseCommand
from webapp.models import PWS

DEFAULT_LEFT_HEADER = '''
<p style="font-size:12px">{PersonInChargeName}<br>
{PersonInChargeJobTitle}<br>
{PWSPhone}<br>
Fax: {PWSFax}<br>
{PWSEmail}</p>
'''

DEFAULT_RIGHT_HEADER = '''
<p style="font-size:12px">{PWSOfficeAddress}<br>
{PWSCity}, {PWSState}, {PWSZip}</p>
'''


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--force', action='store_true', dest='force', default=False, help="Force headers update."),
    )

    def handle(self, *args, **options):
        force = options['force']
        for pws in PWS.objects.all():
            if not pws.letter_left_header_block or force:
                pws.letter_left_header_block = DEFAULT_LEFT_HEADER
            if not pws.letter_right_header_block or force:
                pws.letter_right_header_block = DEFAULT_RIGHT_HEADER
            pws.save()
