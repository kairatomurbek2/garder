# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20150130_0833'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='tester_certificate',
        ),
        migrations.AddField(
            model_name='employee',
            name='certificate',
            field=models.CharField(help_text='May be specified for testers', max_length=30, null=True, verbose_name='Cert. Number', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='employee',
            name='pws',
            field=models.ForeignKey(related_name='employees', blank=True, to='webapp.PWS', help_text='Should be specified for remote administrators to grant them data access', null=True, verbose_name='PWS'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='cv1_gauge_pressure',
            field=models.FloatField(null=True, verbose_name='CV1 Gauge Pressure', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='cv1_leaked',
            field=models.BooleanField(default=False, verbose_name='CV1 Leaked', choices=[(True, b'Leaked'), (False, b'Closed')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='cv1_maintenance',
            field=models.BooleanField(default=False, verbose_name='CV1 Maintenance', choices=[(True, b'Yes'), (False, b'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='cv1_maintenance_pressure',
            field=models.FloatField(null=True, verbose_name='CV1 Maintenance Pressure', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='cv2_gauge_pressure',
            field=models.FloatField(null=True, verbose_name='CV2 Gauge Pressure', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='cv2_leaked',
            field=models.BooleanField(default=False, verbose_name='CV2 Leaked', choices=[(True, b'Leaked'), (False, b'Closed')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='cv2_maintenance',
            field=models.BooleanField(default=False, verbose_name='CV2 Maintenance', choices=[(True, b'Yes'), (False, b'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='cv2_maintenance_pressure',
            field=models.FloatField(null=True, verbose_name='CV2 Maintenance Pressure', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='cv_held_pressure',
            field=models.FloatField(null=True, verbose_name='CV Held Pressure', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='cv_leaked',
            field=models.BooleanField(default=False, verbose_name='CV Leaked', choices=[(True, b'Leaked'), (False, b'Closed')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='cv_maintenance',
            field=models.BooleanField(default=False, verbose_name='CV Maintenance', choices=[(True, b'Yes'), (False, b'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='cv_psi',
            field=models.FloatField(null=True, verbose_name='CV PSI', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='outlet_sov_leaked',
            field=models.BooleanField(default=False, verbose_name='Outlet SOV Leaked', choices=[(True, b'Leaked'), (False, b'Closed')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='pvb_open_pressure',
            field=models.FloatField(null=True, verbose_name='PVB Open Pressure', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='rv_maintenance',
            field=models.BooleanField(default=False, verbose_name='RV Maintenance', choices=[(True, b'Yes'), (False, b'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='rv_opened',
            field=models.BooleanField(default=False, verbose_name='RV Opened', choices=[(True, b'Opened'), (False, b'Closed')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='rv_psi1',
            field=models.FloatField(null=True, verbose_name='RV Pressure 1', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='rv_psi2',
            field=models.FloatField(null=True, verbose_name='RV Pressure 2', blank=True),
            preserve_default=True,
        ),
    ]
