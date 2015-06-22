from django.conf import settings
from django.core.management import BaseCommand
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _

from main.parameters import Groups
from webapp import models


class Command(BaseCommand):
    html_template = 'email_templates/html/unpaid_tests_notification.html'
    plain_template = 'email_templates/plain/unpaid_tests_notification.txt'
    subject = _('Notification about unpaid tests')

    def handle(self, *args, **options):
        testers = models.User.objects.filter(groups__name=Groups.tester)
        for tester in testers:
            unpaid_tests = models.Test.objects.filter(tester=tester, paid=False)
            if unpaid_tests.exists():
                context = {
                    'unpaid_tests': unpaid_tests,
                    'tester': tester,
                    'days': settings.DELETE_UNPAID_TESTS_AFTER_DAYS
                }
                html_content = render_to_string(self.html_template, context)
                plain_content = render_to_string(self.plain_template, context)
                tester.email_user(subject=self.subject,
                                  message=plain_content,
                                  from_email=settings.DEFAULT_FROM_EMAIL,
                                  html_message=html_content)