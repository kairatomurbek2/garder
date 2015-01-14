# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20150114_0718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteuse',
            name='site_use',
            field=models.CharField(max_length=30, verbose_name='Site Use'),
            preserve_default=True,
        ),
    ]
