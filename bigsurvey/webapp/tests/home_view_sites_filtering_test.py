from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client
from django.test.testcases import TestCase
from webapp import models


class HomeViewTest(TestCase):
    fixtures = ['webapp_features/fixtures/test.json']

    def setUp(self):
        self.client = Client()

    def test_pws_admin_sees_only_their_own_sites(self):
        self.admin_logs_in()
        expected_sites = list(models.Site.objects.filter(pws__in=self.admin.employee.pws.all()))
        response = self.client.get(reverse('webapp:home'))
        actual_sites = list(response.context['sites'])
        self.assertListEqual(expected_sites, actual_sites)

    def admin_logs_in(self):
        self.client.login(username='admin', password='admin')
        self.admin = User.objects.get(username='admin')
