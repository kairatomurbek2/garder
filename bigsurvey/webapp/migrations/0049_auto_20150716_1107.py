# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0048_auto_20150716_0822'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='cv1_maintenance',
        ),
        migrations.RemoveField(
            model_name='test',
            name='cv1_maintenance_pressure',
        ),
        migrations.RemoveField(
            model_name='test',
            name='cv2_maintenance',
        ),
        migrations.RemoveField(
            model_name='test',
            name='cv2_maintenance_pressure',
        ),
        migrations.RemoveField(
            model_name='test',
            name='cv_maintenance',
        ),
        migrations.RemoveField(
            model_name='test',
            name='cv_psi',
        ),
        migrations.RemoveField(
            model_name='test',
            name='pvb_open_pressure',
        ),
        migrations.RemoveField(
            model_name='test',
            name='pvb_opened',
        ),
        migrations.RemoveField(
            model_name='test',
            name='rv_maintenance',
        ),
        migrations.AddField(
            model_name='test',
            name='cv1_detail_cv_assembly',
            field=models.BooleanField(default=False, verbose_name='CV Assembly'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='cv1_detail_disk',
            field=models.BooleanField(default=False, verbose_name='Disk'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='cv1_detail_lock_nuts',
            field=models.BooleanField(default=False, verbose_name='Lock Nuts'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='cv1_detail_o_rings',
            field=models.BooleanField(default=False, verbose_name='O-Rings'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='cv1_detail_other',
            field=models.BooleanField(default=False, verbose_name='Other'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='cv1_detail_retainer',
            field=models.BooleanField(default=False, verbose_name='Retainer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='cv1_detail_rubber_parts_kit',
            field=models.BooleanField(default=False, verbose_name='Rubber Parts Kit'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='cv1_detail_seat',
            field=models.BooleanField(default=False, verbose_name='Seat'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='cv1_detail_spring',
            field=models.BooleanField(default=False, verbose_name='Spring'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='cv1_detail_stem_guide',
            field=models.BooleanField(default=False, verbose_name='Stem/Guide'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='cv1_retest_gauge_pressure',
            field=models.DecimalField(null=True, verbose_name='CV1 Retest Gauge Pressure', max_digits=10, decimal_places=1, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='cv2_detail_cv_assembly',
            field=models.BooleanField(default=False, verbose_name='CV Assembly'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='cv2_detail_disk',
            field=models.BooleanField(default=False, verbose_name='Disk'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='cv2_detail_lock_nuts',
            field=models.BooleanField(default=False, verbose_name='Lock Nuts'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='cv2_detail_o_rings',
            field=models.BooleanField(default=False, verbose_name='O-Rings'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='cv2_detail_other',
            field=models.BooleanField(default=False, verbose_name='Other'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='cv2_detail_retainer',
            field=models.BooleanField(default=False, verbose_name='Retainer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='cv2_detail_rubber_parts_kit',
            field=models.BooleanField(default=False, verbose_name='Rubber Parts Kit'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='cv2_detail_seat',
            field=models.BooleanField(default=False, verbose_name='Seat'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='cv2_detail_spring',
            field=models.BooleanField(default=False, verbose_name='Spring'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='cv2_detail_stem_guide',
            field=models.BooleanField(default=False, verbose_name='Stem/Guide'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='cv2_retest_gauge_pressure',
            field=models.DecimalField(null=True, verbose_name='CV2 Retest Gauge Pressure', max_digits=10, decimal_places=1, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='pvb_detail_disk_air_inlet',
            field=models.BooleanField(default=False, verbose_name='Disk, Air Inlet'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='pvb_detail_disk_check_valve',
            field=models.BooleanField(default=False, verbose_name='Disk, Check Valve'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='pvb_detail_guide',
            field=models.BooleanField(default=False, verbose_name='Guide'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='pvb_detail_o_rings',
            field=models.BooleanField(default=False, verbose_name='O-Rings'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='pvb_detail_other',
            field=models.BooleanField(default=False, verbose_name='Other'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='pvb_detail_rubber_parts_kit',
            field=models.BooleanField(default=False, verbose_name='Rubber Parts Kit'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='pvb_detail_rv_assembly',
            field=models.BooleanField(default=False, verbose_name='RV Assembly'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='pvb_detail_seat_check_valve',
            field=models.BooleanField(default=False, verbose_name='Seat, Check Valve'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='pvb_detail_spring_air_inlet',
            field=models.BooleanField(default=False, verbose_name='Spring, Air Inlet'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='pvb_detail_spring_check_valve',
            field=models.BooleanField(default=False, verbose_name='Spring, Check Valve'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='rv_detail_diaphragms',
            field=models.BooleanField(default=False, verbose_name='Diaphragm(s)'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='rv_detail_disk',
            field=models.BooleanField(default=False, verbose_name='Disk'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='rv_detail_guide',
            field=models.BooleanField(default=False, verbose_name='Guide'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='rv_detail_o_rings',
            field=models.BooleanField(default=False, verbose_name='O-Rings'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='rv_detail_other',
            field=models.BooleanField(default=False, verbose_name='Other'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='rv_detail_rubber_parts_kit',
            field=models.BooleanField(default=False, verbose_name='Rubber Parts Kit'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='rv_detail_rv_assembly',
            field=models.BooleanField(default=False, verbose_name='RV Assembly'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='rv_detail_seat',
            field=models.BooleanField(default=False, verbose_name='Seat'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='rv_detail_spring',
            field=models.BooleanField(default=False, verbose_name='Spring'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='paid',
            field=models.BooleanField(default=False, verbose_name='Whether test paid?'),
            preserve_default=True,
        ),
    ]
