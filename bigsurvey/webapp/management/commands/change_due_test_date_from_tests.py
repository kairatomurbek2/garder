from django.core.management import BaseCommand
from webapp.models import Test


class Command(BaseCommand):
    def handle(self, *args, **options):
        tests = Test.objects.filter(paid=True, test_result=True)
        for test in tests:
            test.update_due_test_date()
