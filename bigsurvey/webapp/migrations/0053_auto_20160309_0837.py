# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0052_auto_20160303_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='letter',
            name='already_sent',
            field=models.BooleanField(default=True, verbose_name=b'Already Sent'),
            preserve_default=True,
        ),
    ]
