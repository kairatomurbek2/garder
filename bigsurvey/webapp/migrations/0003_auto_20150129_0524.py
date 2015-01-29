# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20150129_0517'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='survey',
            options={'get_latest_by': 'survey_date', 'verbose_name': 'Survey', 'verbose_name_plural': 'Surveys', 'permissions': (('browse_survey', 'Can browse Survey'), ('add_survey_only_if_doesnt_exist', 'Can add Survey only if it doesnt exist'))},
        ),
    ]
