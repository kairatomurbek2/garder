# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_auto_20150506_0456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='cv1_cleaned',
            field=models.BooleanField(default=True, verbose_name='CV1 Cleaned or Replaced', choices=[(True, b'Cleaned'), (False, b'Replaced')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='cv2_cleaned',
            field=models.BooleanField(default=True, verbose_name='CV2 Cleaned or Replaced', choices=[(True, b'Cleaned'), (False, b'Replaced')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='pvb_cleaned',
            field=models.BooleanField(default=True, verbose_name='PVB Cleaned or Replaced', choices=[(True, b'Cleaned'), (False, b'Replaced')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='rv_cleaned',
            field=models.BooleanField(default=True, verbose_name='RV Cleaned or Replaced', choices=[(True, b'Cleaned'), (False, b'Replaced')]),
            preserve_default=True,
        ),
    ]
