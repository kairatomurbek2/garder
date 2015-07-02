from datetime import datetime, timedelta

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase
from django.core import mail
from django.utils.translation import ugettext as _

from webapp import models


class TestManagementCommands(TestCase):
    def setUp(self):
        call_command('restore_db')

    def test_testers_notifications(self):
        call_command('notify_testers')
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.subject, _('Notification about unpaid tests'))
        self.assertEqual(email.from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(email.to, ['tester@example.com'])
        self.assertIn('tester tester', email.body)
        self.assertIn('Washington, White House, Digester', email.body)
        self.assertIn('2015-06-01', email.body)

    def test_deleting_unpaid_tests(self):
        test = models.Test.objects.last()
        test.pk = None
        test.paid = False
        test.save()
        test.test_date = datetime.now() - timedelta(days=settings.DELETE_UNPAID_TESTS_AFTER_DAYS + 1)
        test.save()
        call_command('delete_unpaid_tests')
        self.assertFalse(models.Test.objects.filter(pk=test.pk).exists())