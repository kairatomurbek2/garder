# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hazard',
            options={'verbose_name': 'Hazard', 'verbose_name_plural': 'Hazards', 'permissions': (('browse_hazard', 'Can browse Hazard'), ('access_to_all_hazards', 'Has access to all Hazards'), ('access_to_pws_hazards', "Has access to his PWS's Hazards"), ('access_to_own_hazards', 'Has access to his own Hazards'), ('access_to_site_hazards', "Has access to Site's Hazards"))},
        ),
        migrations.AlterModelOptions(
            name='site',
            options={'verbose_name': 'Site', 'verbose_name_plural': 'Sites', 'permissions': (('browse_site', 'Can browse Site'), ('access_to_all_sites', 'Can browse all Sites'), ('access_to_pws_sites', "Has access his PWS's Sites"), ('access_to_survey_sites', 'Has access Sites that he inspects'), ('access_to_test_sites', 'Has access Sites that he tests'), ('access_to_import', 'Can import Sites from Excel file'), ('assign_surveyor', 'Can assign Surveyor to Site'), ('assign_tester', 'Can assign Tester to Site'), ('commit_site', 'Can commit Site'))},
        ),
        migrations.AlterModelOptions(
            name='survey',
            options={'get_latest_by': 'survey_date', 'verbose_name': 'Survey', 'verbose_name_plural': 'Surveys', 'permissions': (('browse_survey', 'Can browse Survey'), ('access_to_all_surveys', 'Has access all Surveys'), ('access_to_pws_surveys', "Has access to his PWS's Surveys"), ('access_to_own_surveys', 'Has access to own Surveys'), ('add_many_surveys_per_site', 'Can add many Surveys per Site'))},
        ),
    ]
