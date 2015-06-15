# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0021_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='pws',
            name='plumber_packet_address',
            field=models.CharField(max_length=100, null=True, verbose_name='Plumber Packet Address', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pws',
            name='plumber_packet_location',
            field=models.CharField(max_length=100, null=True, verbose_name='Plumber Packet Location', blank=True),
            preserve_default=True,
        ),
    ]
