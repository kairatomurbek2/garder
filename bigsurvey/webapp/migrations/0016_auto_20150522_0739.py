# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0015_test_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='air_inlet_retest_psi',
            field=models.FloatField(null=True, verbose_name='Air Inlet Retest PSI', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='cv_retest_psi',
            field=models.FloatField(null=True, verbose_name='CV Retest PSI', blank=True),
            preserve_default=True,
        ),
    ]
