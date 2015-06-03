from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.template.loader import render_to_string
from main.parameters import Groups
from webapp import models
from django.utils.translation import ugettext as _


class Command(BaseCommand):
    html_template = 'email_templates/html/unpaid_tests_notification.html'
    plain_template = 'email_templates/plain/unpaid_tests_notification.txt'
    subject = _('Notification about unpaid tests')

    def handle(self, *args, **options):
        testers = models.User.objects.filter(groups__name=Groups.tester)
        for tester in testers:
            unpaid_tests = models.Test.objects.filter(tester=tester)
            if unpaid_tests.exists():
                context = {
                    'unpaid_tests': unpaid_tests,
                    'tester': tester
                }
                html_content = render_to_string(self.html_template, context)
                plain_content = render_to_string(self.plain_template, context)
                send_mail(subject=self.subject,
                          message=plain_content,
                          from_email=settings.DEFAULT_FROM_EMAIL,
                          recipient_list=[tester.employee.email],
                          html_message=html_content)