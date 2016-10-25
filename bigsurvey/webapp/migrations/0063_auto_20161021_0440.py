# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def copy_data(apps, schema_editor):
    hazards = apps.get_model("webapp", "Hazard")
    devices = apps.get_model("webapp", "BPDevice")
    for i in xrange(0, len(devices.objects.all())):
        hazard, device = hazards.objects.all()[i], devices.objects.all()[i]
        hazard.due_test_date = device.due_test_date
        hazard.save()


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0062_hazard_due_test_date'),
    ]

    operations = [
        migrations.RunPython(copy_data),
    ]
