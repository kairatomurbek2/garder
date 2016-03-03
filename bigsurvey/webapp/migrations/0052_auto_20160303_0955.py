# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0051_add_browse_hazard_list_permission'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hazard',
            options={'verbose_name': 'Hazard', 'verbose_name_plural': 'Hazards', 'permissions': (('browse_hazard', 'Can browse Hazard'), ('browse_hazard_list', 'Can browse Hazard List'), ('access_to_all_hazards', 'Has access to all Hazards'), ('access_to_pws_hazards', "Has access to PWS's Hazards"), ('access_to_multiple_pws_hazards', "Has access to multiple PWS' Hazards"))},
        ),
        migrations.AlterModelOptions(
            name='testercert',
            options={'verbose_name': 'Tester Certificate', 'verbose_name_plural': 'Tester Certificates', 'permissions': (('access_to_all_tester_certs', "Access to all testers' certs"), ('access_to_pws_tester_certs', "Access to own PWS' testers' certs"), ('can_own_cert_kit', 'Can own cert kit'))},
        ),
        migrations.AlterModelOptions(
            name='testkit',
            options={'verbose_name': 'Test Kit', 'verbose_name_plural': 'Test Kits', 'permissions': (('access_to_all_test_kits', "Access to all testers' kits"), ('access_to_pws_test_kits', "Access to own PWS' testers' kits"), ('can_own_test_kit', 'Can own test kit'))},
        ),
    ]
