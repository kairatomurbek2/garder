import json
from django.core.management import call_command
from django.conf import settings
from django.test import TestCase
from webapp import models
from webapp.actions.builders import SampleSitesJsonUploaderBuilder


class TestSampleSitesJsonUploader(TestCase):
    def setUp(self):
        self.raw_json = settings.SAMPLE_DATA_JSON
        call_command('loaddata', 'webapp_features/fixtures/test.json')
        pws = models.PWS.objects.all()[0]
        self.action = SampleSitesJsonUploaderBuilder.load_sample_data(pws)

    def test_action_creates_sites_from_json_file(self):
        with open(self.raw_json) as raw_data:
            json_data = raw_data.read()
        loaded_json = json.loads(json_data)
        result = self.action.execute()
        self.assertEqual(len(loaded_json), result)
