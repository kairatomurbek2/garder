# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0035_remove_testpricehistory_pws'),
    ]

    operations = [
        migrations.AddField(
            model_name='hazard',
            name='due_install_date',
            field=models.DateField(null=True, verbose_name='Due Install Date', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bpdevice',
            name='due_test_date',
            field=models.DateField(null=True, verbose_name='Due Test Date', blank=True),
            preserve_default=True,
        ),
    ]
