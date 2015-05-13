# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0011_auto_20150512_0639'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='regulation',
            options={'ordering': ('name',), 'verbose_name': 'Regulation Type', 'verbose_name_plural': 'Regulation Types', 'permissions': (('browse_regulation', 'Can browse Regulation Type'),)},
        ),
    ]
