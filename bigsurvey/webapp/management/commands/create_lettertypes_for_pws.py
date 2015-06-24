from django.core.management import BaseCommand
from webapp.models import LetterType, PWS


class Command(BaseCommand):
    def handle(self, *args, **options):
        default_letter_types = LetterType.objects.filter(pws=None)
        for pws in PWS.objects.all():
            for default_letter_type in default_letter_types:
                if not pws.letter_types.filter(letter_type=default_letter_type.letter_type).exists():
                    letter_type = LetterType()
                    letter_type.pws = pws
                    letter_type.letter_type = default_letter_type.letter_type
                    letter_type.header = default_letter_type.header
                    letter_type.template = default_letter_type.template
                    letter_type.save()