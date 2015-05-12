# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0010_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='cust_number',
            field=models.CharField(help_text="Customer's Number", max_length=15, verbose_name='Number', db_index=True),
            preserve_default=True,
        ),
    ]
