# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0024_auto_20160114_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bpdevice',
            name='bp_type_present',
            field=models.CharField(max_length=15, verbose_name='BP Type Present', choices=[(b'Air Gap', b'Air Gap'), (b'AVB', b'AVB'), (b'DC', b'DC'), (b'DCDA', b'DCDA'), (b'HBVB', b'HBVB'), (b'PVB', b'PVB'), (b'RP', b'RP'), (b'RPDA', b'RPDA'), (b'SVB', b'SVB')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='bp_device',
            field=models.ForeignKey(related_name='tests', verbose_name='BP Device', to='webapp.BPDevice'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='cv1_cleaned',
            field=models.CharField(default=b'0', max_length=255, verbose_name='CV1 Cleaned or Replaced', choices=[(b'0', 'Tested Only'), (b'1', 'Cleaned only'), (b'2', 'Maintenance')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='cv2_cleaned',
            field=models.CharField(default=b'0', max_length=255, verbose_name='CV2 Cleaned or Replaced', choices=[(b'0', 'Tested Only'), (b'1', 'Cleaned only'), (b'2', 'Maintenance')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='pvb_cleaned',
            field=models.CharField(default=b'0', max_length=255, verbose_name='PVB Cleaned or Replaced', choices=[(b'0', 'Tested Only'), (b'1', 'Cleaned only'), (b'2', 'Maintenance')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='rv_cleaned',
            field=models.CharField(default=b'0', max_length=255, verbose_name='RV Cleaned or Replaced', choices=[(b'0', 'Tested Only'), (b'1', 'Cleaned only'), (b'2', 'Maintenance')]),
            preserve_default=True,
        ),
    ]
