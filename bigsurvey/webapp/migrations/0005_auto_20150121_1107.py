# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_auto_20150120_0934'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='survey',
            options={'get_latest_by': 'survey_date', 'verbose_name': 'Survey', 'verbose_name_plural': 'Surveys'},
        ),
    ]
