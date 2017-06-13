# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0070_auto_20170613_0224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='cust_address1',
            field=models.CharField(max_length=100, null=True, verbose_name='Customer Name 2', blank=True),
            preserve_default=True,
        ),
    ]
