from django.core.management import BaseCommand
from django.db import connection
from webapp.raw_sql_queries import SetDueInstallTestDateQuery


class Command(BaseCommand):
    def handle(self, *args, **options):
        cursor = connection.cursor()
        query = SetDueInstallTestDateQuery.get_query(connection.vendor)
        cursor.execute(query)
