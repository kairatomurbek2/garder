# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0065_pricehistory_pws'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='apt',
            field=models.CharField(max_length=50, null=True, verbose_name='Service Site Apt', blank=True),
            preserve_default=True,
        ),
    ]
