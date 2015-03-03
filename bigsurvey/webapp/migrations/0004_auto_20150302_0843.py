# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20150225_0444'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='letter',
            options={'verbose_name': 'Letter', 'verbose_name_plural': 'Letters', 'permissions': (('browse_letter', 'Can browse Letter'), ('send_letter', 'Can send Letter'))},
        ),
        migrations.RemoveField(
            model_name='letter',
            name='survey',
        ),
        migrations.AddField(
            model_name='letter',
            name='hazard',
            field=models.ForeignKey(related_name='letters', verbose_name='Hazard', blank=True, to='webapp.Hazard', null=True),
            preserve_default=True,
        ),
    ]
