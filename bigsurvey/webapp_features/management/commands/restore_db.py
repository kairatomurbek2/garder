from django.core.management import BaseCommand, call_command

from webapp import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        models.Site.objects.all().delete()
        call_command('loaddata', 'test', interactive=False, verbosity=0)