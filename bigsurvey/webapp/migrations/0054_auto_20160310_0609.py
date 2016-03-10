# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0053_auto_20160309_0837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='letter',
            name='already_sent',
            field=models.BooleanField(default=False, verbose_name=b'Already Sent'),
            preserve_default=True,
        ),
    ]
