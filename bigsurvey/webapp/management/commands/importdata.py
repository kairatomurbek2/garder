from django.core.management.base import BaseCommand
from webapp import models


class Command(BaseCommand):
    help = '[STUB] Imports data (currently does nothing)'

    def handle(self, *args, **options):
        pass