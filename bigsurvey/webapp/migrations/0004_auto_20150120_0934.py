# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20150120_0757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='potable_present',
            field=models.BooleanField(default=True, verbose_name='Potable Present', choices=[(True, b'Yes'), (False, b'No')]),
            preserve_default=True,
        ),
    ]
