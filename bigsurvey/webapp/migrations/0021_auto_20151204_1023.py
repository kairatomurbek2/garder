# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0020_auto_20151203_0753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hazard',
            name='model_no',
            field=models.CharField(max_length=30, null=True, verbose_name='BP Model No.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hazard',
            name='serial_no',
            field=models.CharField(max_length=30, null=True, verbose_name='BP Serial No.', blank=True),
            preserve_default=True,
        ),
    ]
