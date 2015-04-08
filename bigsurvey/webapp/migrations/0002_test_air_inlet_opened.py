# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='air_inlet_opened',
            field=models.BooleanField(default=False, verbose_name='Air Inlet Opened', choices=[(True, b'Yes'), (False, b'No')]),
            preserve_default=True,
        ),
    ]
