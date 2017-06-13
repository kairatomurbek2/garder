# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0069_auto_20170613_0219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='cust_zip',
            field=models.CharField(max_length=10, null=True, verbose_name='Mailing ZIP', blank=True),
            preserve_default=True,
        ),
    ]
