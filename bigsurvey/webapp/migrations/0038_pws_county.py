# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0037_auto_20160202_0659'),
    ]

    operations = [
        migrations.AddField(
            model_name='pws',
            name='county',
            field=models.CharField(max_length=100, null=True, verbose_name='County', blank=True),
            preserve_default=True,
        ),
    ]
