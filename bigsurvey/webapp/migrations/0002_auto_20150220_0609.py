# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='site',
            options={'verbose_name': 'Site', 'verbose_name_plural': 'Sites', 'permissions': (('browse_site', 'Can browse Site'), ('access_to_all_sites', 'Has access to all Sites'), ('access_to_pws_sites', "Has access to PWS's Sites"), ('access_to_survey_sites', 'Has access to Sites that he inspects'), ('access_to_test_sites', 'Has access to Sites that he tests'), ('access_to_import', 'Can import Sites from Excel file'), ('assign_surveyor', 'Can assign Surveyor to Site'), ('assign_tester', 'Can assign Tester to Site'), ('commit_site', 'Can commit Site'), ('access_to_batch_update', 'Has access to batch update'))},
        ),
    ]
