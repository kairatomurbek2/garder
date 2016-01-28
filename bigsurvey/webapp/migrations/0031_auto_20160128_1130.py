# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0030_testpricehistory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pws',
            name='price',
        ),
        migrations.AddField(
            model_name='test',
            name='price',
            field=models.DecimalField(default=Decimal('0'), verbose_name='Price', max_digits=7, decimal_places=2),
            preserve_default=True,
        ),
    ]
