# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address1',
            field=models.CharField(max_length=100, verbose_name='Address 1'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='address2',
            field=models.CharField(max_length=100, null=True, verbose_name='Address 2', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='address1',
            field=models.CharField(max_length=100, verbose_name='Address 1'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='address2',
            field=models.CharField(max_length=100, null=True, verbose_name='Address 2', blank=True),
            preserve_default=True,
        ),
    ]
