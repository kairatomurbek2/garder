# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_auto_20150505_1008'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='letter',
            options={'verbose_name': 'Letter', 'verbose_name_plural': 'Letters', 'permissions': (('browse_letter', 'Can browse Letter'), ('send_letter', 'Can send Letter'), ('pws_letter_access', 'Has access to pws letters'))},
        ),
        migrations.AddField(
            model_name='letter',
            name='already_sent',
            field=models.BooleanField(default=False, verbose_name=b'Already Sent'),
            preserve_default=True,
        ),
    ]
