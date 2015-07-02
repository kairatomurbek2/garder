# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0032_auto_20150701_0828'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ImportProgress',
        ),
        migrations.AddField(
            model_name='importlog',
            name='progress',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
