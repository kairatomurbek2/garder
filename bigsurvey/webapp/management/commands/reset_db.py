from django.core.management.base import CommandError
from django.core.management.base import BaseCommand
from main.settings_test import DATABASES


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
            import os
            try:
                print "Unlinking SQLite3 database"
                os.unlink(DATABASES['default']['NAME'])
            except OSError:
                print "Error: %s - %s" % (OSError.errno, OSError.message)
        else:
            raise CommandError("Only SQLite3 supported for reset")

        print "Unlink success"