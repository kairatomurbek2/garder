# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0030_auto_20150624_1202'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='survey',
            options={'ordering': ('-survey_date', '-id'), 'get_latest_by': 'survey_date', 'verbose_name': 'Survey', 'verbose_name_plural': 'Surveys', 'permissions': (('browse_survey', 'Can browse Survey'), ('access_to_all_surveys', 'Has access to all Surveys'), ('access_to_pws_surveys', "Has access to PWS's Surveys"), ('access_to_own_surveys', 'Has access to own Surveys'))},
        ),
    ]
