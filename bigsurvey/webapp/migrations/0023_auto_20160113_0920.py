# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0022_auto_20151207_0900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='cv1_cleaned',
            field=models.CharField(default=b'0', max_length=255, verbose_name='CV1 Cleaned or Replaced', choices=[(b'0', 'Tested Only'), (b'1', 'Cleaned only'), (b'2', 'Replaced')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='cv2_cleaned',
            field=models.CharField(default=b'0', max_length=255, verbose_name='CV2 Cleaned or Replaced', choices=[(b'0', 'Tested Only'), (b'1', 'Cleaned only'), (b'2', 'Replaced')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='pvb_cleaned',
            field=models.CharField(default=b'0', max_length=255, verbose_name='PVB Cleaned or Replaced', choices=[(b'0', 'Tested Only'), (b'1', 'Cleaned only'), (b'2', 'Replaced')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='rv_cleaned',
            field=models.CharField(default=b'0', max_length=255, verbose_name='RV Cleaned or Replaced', choices=[(b'0', 'Tested Only'), (b'1', 'Cleaned only'), (b'2', 'Replaced')]),
            preserve_default=True,
        ),
    ]
