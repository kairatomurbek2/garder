from django.core.management import BaseCommand, call_command
from django.db.models.loading import get_models


class Command(BaseCommand):
    def handle(self, *args, **options):
        models = get_models()
        for model in models:
            model.objects.all().delete()
        call_command('loaddata', 'test', interactive=False, verbosity=1)