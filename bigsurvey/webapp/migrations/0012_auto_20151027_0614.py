# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0011_auto_20151027_0535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='meter_number',
            field=models.CharField(help_text='Meter Number', max_length=50, null=True, verbose_name='Meter Number', blank=True),
            preserve_default=True,
        ),
    ]
