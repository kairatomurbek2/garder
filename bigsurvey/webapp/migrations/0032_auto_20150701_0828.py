# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0031_auto_20150626_0517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hazard',
            name='latitude',
            field=models.FloatField(null=True, verbose_name='Latitude', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hazard',
            name='longitude',
            field=models.FloatField(null=True, verbose_name='Longitude', blank=True),
            preserve_default=True,
        ),
    ]
