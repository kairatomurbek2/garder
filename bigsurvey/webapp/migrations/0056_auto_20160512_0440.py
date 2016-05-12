# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0055_importlog_duplicates_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='importlog',
            name='duplicates_count',
            field=models.IntegerField(default=0, verbose_name='Duplicates number', blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='site',
            unique_together=set([('pws', 'cust_number', 'address1', 'street_number')]),
        ),
    ]
