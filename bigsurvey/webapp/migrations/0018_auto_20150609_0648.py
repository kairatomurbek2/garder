# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0017_pws_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pws',
            name='price',
            field=models.DecimalField(default=Decimal('0'), verbose_name="Test's Price", max_digits=10, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
