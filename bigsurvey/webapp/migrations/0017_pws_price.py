# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0016_auto_20150522_0739'),
    ]

    operations = [
        migrations.AddField(
            model_name='pws',
            name='price',
            field=models.IntegerField(default=0, max_length=10, null=True, verbose_name='Price', blank=True),
            preserve_default=True,
        ),
    ]
