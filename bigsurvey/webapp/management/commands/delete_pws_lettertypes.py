from django.core.management import BaseCommand
from webapp.models import LetterType


class Command(BaseCommand):
    help = """
    Deletes PWS letter types
    """

    def handle(self, *args, **options):
        LetterType.objects.exclude(pws=None).delete()