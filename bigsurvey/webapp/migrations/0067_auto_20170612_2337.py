# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0066_auto_20170612_0346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='cust_city',
            field=models.CharField(max_length=30, null=True, verbose_name='Mailing City', blank=True),
            preserve_default=True,
        ),
    ]
