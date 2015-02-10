# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_auto_20150206_1112'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='email',
            field=models.CharField(max_length=15, null=True, verbose_name='Email', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='fax',
            field=models.CharField(max_length=15, null=True, verbose_name='Fax', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(max_length=15, null=True, verbose_name='Phone', blank=True),
            preserve_default=True,
        ),
    ]
