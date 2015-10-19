# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_auto_20151014_0944'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'verbose_name': 'Employee', 'verbose_name_plural': 'Employees', 'permissions': (('browse_user', 'Can browse Users'), ('access_to_adminpanel', 'Can log into Admin Panel'), ('access_to_all_users', 'Has access to all Users'), ('access_to_pws_users', "Has access to PWS's Users"), ('access_to_multiple_pws_users', 'Has access to Users from multiple PWS'))},
        ),
        migrations.AlterModelOptions(
            name='hazard',
            options={'verbose_name': 'Hazard', 'verbose_name_plural': 'Hazards', 'permissions': (('browse_hazard', 'Can browse Hazard'), ('access_to_all_hazards', 'Has access to all Hazards'), ('access_to_pws_hazards', "Has access to PWS's Hazards"), ('access_to_multiple_pws_hazards', "Has access to multiple PWS' Hazards"), ('change_all_info_about_hazard', 'Can change all information about Hazard'))},
        ),
        migrations.AlterModelOptions(
            name='letter',
            options={'verbose_name': 'Letter', 'verbose_name_plural': 'Letters', 'permissions': (('browse_letter', 'Can browse Letter'), ('send_letter', 'Can send Letter'), ('pws_letter_access', 'Has access to pws letters'), ('multiple_pws_letter_access', "Has access to multiple pws' letters"), ('full_letter_access', 'Has access to all letters'))},
        ),
        migrations.AlterModelOptions(
            name='lettertype',
            options={'ordering': ('letter_type',), 'verbose_name': 'Letter Type', 'verbose_name_plural': 'Letter Types', 'permissions': (('browse_lettertype', 'Can browse Letter Type'), ('access_to_all_lettertypes', 'Has access to all Letter Types'), ('access_to_pws_lettertypes', "Has access to PWS' Letter Types"))},
        ),
        migrations.AlterModelOptions(
            name='site',
            options={'verbose_name': 'Site', 'verbose_name_plural': 'Sites', 'permissions': (('browse_site', 'Can browse Site'), ('access_to_all_sites', 'Has access to all Sites'), ('access_to_pws_sites', "Has access to PWS's Sites"), ('access_to_multiple_pws_sites', "Has access to multiple PWS' Sites"), ('access_to_site_by_customer_account', 'Has access to Site through Customer Account'), ('access_to_import', 'Can import Sites from Excel file'), ('access_to_batch_update', 'Has access to batch update'), ('change_all_info_about_site', 'Can change all information about Site'))},
        ),
        migrations.AlterModelOptions(
            name='survey',
            options={'ordering': ('-survey_date', '-id'), 'get_latest_by': 'survey_date', 'verbose_name': 'Survey', 'verbose_name_plural': 'Surveys', 'permissions': (('browse_survey', 'Can browse Survey'), ('access_to_all_surveys', 'Has access to all Surveys'), ('access_to_pws_surveys', "Has access to PWS's Surveys"), ('access_to_multiple_pws_surveys', "Has access to multiple PWS' Surveys"), ('access_to_own_surveys', 'Has access to own Surveys'))},
        ),
        migrations.AlterModelOptions(
            name='test',
            options={'ordering': ('-test_date', '-id'), 'verbose_name': 'Test', 'verbose_name_plural': 'Tests', 'permissions': (('browse_test', 'Can browse Test'), ('access_to_all_tests', 'Has access to all Tests'), ('access_to_pws_tests', "Has access to PWS's Tests"), ('access_to_multiple_pws_tests', "Has access to multiple PWS' Tests"), ('access_to_own_tests', 'Has access to own Tests'))},
        ),
    ]
