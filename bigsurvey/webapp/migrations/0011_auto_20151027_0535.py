# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0010_auto_20151026_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='meter_size',
            field=models.CharField(help_text='Meter Size', max_length=50, null=True, verbose_name='Meter Size', blank=True),
            preserve_default=True,
        ),
    ]
