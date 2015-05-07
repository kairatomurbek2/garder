from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command('loaddata', 'test', interactive=False, verbosity=1)