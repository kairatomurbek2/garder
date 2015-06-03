from datetime import datetime, timedelta
from django.conf import settings
from django.core.management import BaseCommand
from webapp import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        deadline = datetime.now() - timedelta(days=settings.DELETE_UNPAID_TESTS_AFTER_DAYS)
        unpaid_tests = models.Test.objects.filter(paid=False, test_date__lt=deadline)
        unpaid_tests.delete()
