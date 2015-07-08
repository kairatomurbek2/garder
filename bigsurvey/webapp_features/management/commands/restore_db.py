from django.core.management import BaseCommand, call_command
from django.db.models.loading import get_models, get_app


class Command(BaseCommand):
    def handle(self, *args, **options):
        webapp = get_app('webapp')
        for model in get_models(webapp):
            model.objects.all().delete()
        call_command('loaddata', 'test', interactive=False, verbosity=1)
        call_command('create_lettertypes_for_pws', interactive=False, verbosity=1)
