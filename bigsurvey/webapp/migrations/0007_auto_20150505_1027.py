# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_auto_20150505_1025'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='letter',
            options={'verbose_name': 'Letter', 'verbose_name_plural': 'Letters', 'permissions': (('browse_letter', 'Can browse Letter'), ('send_letter', 'Can send Letter'), ('pws_letter_access', 'Has access to pws letters'), ('full_letter_access', 'Has access to all letters'))},
        ),
    ]
