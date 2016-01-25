# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0027_auto_20160122_1004'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='letter_type',
            field=models.ForeignKey(related_name='survey_letter_types', verbose_name='Letter Type', blank=True, to='webapp.LetterType', null=True),
            preserve_default=True,
        ),
    ]
