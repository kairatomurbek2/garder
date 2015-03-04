# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_auto_20150303_1237'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='last_survey_date',
            field=models.DateField(null=True, verbose_name='Last survey date', blank=True),
            preserve_default=True,
        ),
    ]
