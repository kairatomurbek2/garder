# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20150130_0615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='letter',
            name='survey',
            field=models.ForeignKey(related_name='letters', verbose_name='Survey', blank=True, to='webapp.Survey', null=True),
            preserve_default=True,
        ),
    ]
