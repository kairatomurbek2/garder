# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0013_auto_20151028_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='apt',
            field=models.CharField(help_text="Site Address's Apartment", max_length=30, null=True, verbose_name='Apt', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='cust_apt',
            field=models.CharField(help_text="Customer's Apartment", max_length=30, null=True, verbose_name='Customer Apt', blank=True),
            preserve_default=True,
        ),
    ]