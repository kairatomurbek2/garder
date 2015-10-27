# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0009_invite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assemblystatus',
            name='assembly_status',
            field=models.CharField(max_length=50, verbose_name='Assembly Status'),
            preserve_default=True,
        ),
    ]
