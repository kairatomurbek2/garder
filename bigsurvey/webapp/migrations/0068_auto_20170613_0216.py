# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0067_auto_20170612_2337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='cust_address2',
            field=models.CharField(max_length=100, null=True, verbose_name='Mailing Address', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='cust_apt',
            field=models.CharField(max_length=50, null=True, verbose_name='Mailing Site Apt', blank=True),
            preserve_default=True,
        ),
    ]
