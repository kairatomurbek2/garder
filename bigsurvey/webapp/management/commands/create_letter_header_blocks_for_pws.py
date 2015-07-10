from django.core.management import BaseCommand
from webapp.models import PWS


DEFAULT_LEFT_HEADER = '''
<p style="font-size:12px">{BaileeName}<br>
{BaileeJobTitle}<br>
{PWSPhone}<br>
Fax: {PWSFax}<br>
{PWSEmail}</p>
'''

DEFAULT_RIGHT_HEADER = '''
<p style="font-size:12px">{PWSOfficeAddress}<br>
{PWSCity}, {PWSState}, {PWSZip}</p>
'''


class Command(BaseCommand):
    def handle(self, *args, **options):
        for pws in PWS.objects.all():
            if not pws.letter_left_header_block:
                pws.letter_left_header_block = DEFAULT_LEFT_HEADER
            if not pws.letter_right_header_block:
                pws.letter_right_header_block = DEFAULT_RIGHT_HEADER
            pws.save()