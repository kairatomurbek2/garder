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
            options={'verbose_name': 'Site', 'verbose_name_plural': 'Sites', 'permissions': (('browse_site', 'Can browse Site'), ('browse_all_sites', 'Can browse all Sites'), ('browse_pws_sites', 'Can browse Sites from his PWS'), ('browse_surv_sites', 'Can browse Sites that he inspects'), ('browse_test_sites', 'Can browse Sites that he tests'), ('access_to_import', 'Can import Sites from Excel file'), ('assign_surveyor', 'Can assign Surveyor to Site'), ('assign_tester', 'Can assign Tester to Site'), ('commit_site', 'Can commit Site'))},
        ),
    ]
