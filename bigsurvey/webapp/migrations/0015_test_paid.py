# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0014_importprogress'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='paid',
            field=models.BooleanField(default=False, verbose_name='Was test paid?'),
            preserve_default=True,
        ),
    ]
