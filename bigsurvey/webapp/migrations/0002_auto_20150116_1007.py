# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hazard',
            name='BPPresent',
        ),
        migrations.RemoveField(
            model_name='site',
            name='address',
        ),
        migrations.RemoveField(
            model_name='site',
            name='street_address',
        ),
        migrations.RemoveField(
            model_name='site',
            name='street_number',
        ),
        migrations.AddField(
            model_name='hazard',
            name='location1',
            field=models.CharField(default='Some Location', max_length=70, verbose_name='location 1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hazard',
            name='location2',
            field=models.CharField(max_length=70, null=True, verbose_name='location 2', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='site',
            name='address1',
            field=models.CharField(default='Some Address', max_length=50, verbose_name='Address 1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='site',
            name='address2',
            field=models.CharField(max_length=50, null=True, verbose_name='Address 2', blank=True),
            preserve_default=True,
        ),
    ]
