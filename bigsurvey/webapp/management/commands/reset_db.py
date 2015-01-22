from django.core.management.base import CommandError
from django.core.management.base import BaseCommand
from main.settings_test import DATABASES
import os


class Command(BaseCommand):
    help = "Resets a database."

    def handle(self, *args, **options):
        """
        Resets a database.

        Note: Transaction wrappers are in reverse as a work around for
        autocommit, anybody know how to do this the right way?
        """

        engine = DATABASES['default']['ENGINE']

        if 'sqlite3' in engine:
            if os.path.exists(DATABASES['default']['NAME']):
                try:
                    print "Unlinking %s" % DATABASES['default']['NAME']
                    os.unlink(DATABASES['default']['NAME'])
                    print "Unlink success"
                except OSError:
                    raise CommandError("Cannot unlink %s. Please unlink it manually and retry" % DATABASES['default']['NAME'])
        else:
            raise CommandError("Only SQLite3 can be used in RAM-disk")