# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20150116_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='zip',
            field=models.CharField(max_length=10, verbose_name='ZIP'),
            preserve_default=True,
        ),
    ]
