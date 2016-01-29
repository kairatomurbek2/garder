# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0031_auto_20160128_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='testpricehistory',
            name='pws',
            field=models.ForeignKey(verbose_name='PWS', blank=True, to='webapp.PWS', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='testpricehistory',
            name='price',
            field=models.DecimalField(default=Decimal('5'), verbose_name='Price', max_digits=7, decimal_places=2),
            preserve_default=True,
        ),
    ]
