# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20150201_1350'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sitestatus',
            old_name='activity_type',
            new_name='site_status',
        ),
    ]
