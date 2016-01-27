from django.conf import settings
from django.core import serializers


class SampleSitesJsonUploader(object):
    pws = None

    def execute(self):
        with open(settings.SAMPLE_DATA_JSON) as sample_data:
            json_data = sample_data.read()
        count = 0
        for deserialized_object in serializers.deserialize("json", json_data):
            deserialized_object.object.pws_id = self.pws.pk
            deserialized_object.object.save()
            count += 1
        return count
