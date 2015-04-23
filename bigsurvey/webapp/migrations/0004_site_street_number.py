# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20150408_1106'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='street_number',
            field=models.CharField(max_length=100, null=True, verbose_name='Street Number', blank=True),
            preserve_default=True,
        ),
    ]
