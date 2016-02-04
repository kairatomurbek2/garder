# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0037_auto_20160202_0659'),
    ]

    operations = [
        migrations.AddField(
            model_name='hazard',
            name='letter_type',
            field=models.ForeignKey(related_name='hazards', verbose_name='Letter Type', blank=True, to='webapp.LetterType', null=True),
            preserve_default=True,
        ),
    ]
