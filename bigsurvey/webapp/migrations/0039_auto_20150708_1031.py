# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0038_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='air_inlet_psi',
            field=models.DecimalField(null=True, verbose_name='Air Inlet PSI', max_digits=10, decimal_places=1, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='air_inlet_retest_psi',
            field=models.DecimalField(null=True, verbose_name='Air Inlet Retest PSI', max_digits=10, decimal_places=1, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='cv1_gauge_pressure',
            field=models.DecimalField(null=True, verbose_name='CV1 Gauge Pressure', max_digits=10, decimal_places=1, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='cv1_maintenance_pressure',
            field=models.DecimalField(null=True, verbose_name='CV1 Maintenance Pressure', max_digits=10, decimal_places=1, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='cv2_gauge_pressure',
            field=models.DecimalField(null=True, verbose_name='CV2 Gauge Pressure', max_digits=10, decimal_places=1, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='cv2_maintenance_pressure',
            field=models.DecimalField(null=True, verbose_name='CV2 Maintenance Pressure', max_digits=10, decimal_places=1, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='cv_held_pressure',
            field=models.DecimalField(null=True, verbose_name='CV Held Pressure', max_digits=10, decimal_places=1, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='cv_psi',
            field=models.DecimalField(null=True, verbose_name='CV PSI', max_digits=10, decimal_places=1, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='cv_retest_psi',
            field=models.DecimalField(null=True, verbose_name='CV Retest PSI', max_digits=10, decimal_places=1, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='pvb_open_pressure',
            field=models.DecimalField(null=True, verbose_name='PVB Open Pressure', max_digits=10, decimal_places=1, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='rv_psi1',
            field=models.DecimalField(null=True, verbose_name='RV Pressure 1', max_digits=10, decimal_places=1, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='rv_psi2',
            field=models.DecimalField(null=True, verbose_name='RV Pressure 2', max_digits=10, decimal_places=1, blank=True),
            preserve_default=True,
        ),
    ]
