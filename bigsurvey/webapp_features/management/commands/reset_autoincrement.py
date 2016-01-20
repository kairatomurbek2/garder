from django.core.management import BaseCommand
from django.db import connection
from webapp.raw_sql_queries import ResetAutoincrementFieldsForTesting


class Command(BaseCommand):
    def handle(self, *args, **options):
        cursor = connection.cursor()
        try:
            query = ResetAutoincrementFieldsForTesting.get_query(connection.vendor)
            cursor.execute(query)
        except NotImplementedError:
            print """Can not reset autoincrement fields for %s database type.
              Please implement corresponding methods in ResetAutoincrementFieldsForTesting class
              from webapp/raw_sql_queries.py, or use SQLite database for testing purposes.""" % connection.vendor
