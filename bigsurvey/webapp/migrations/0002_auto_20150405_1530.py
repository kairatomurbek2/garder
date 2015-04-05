# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inspection',
            name='assigned_by',
        ),
        migrations.RemoveField(
            model_name='inspection',
            name='assigned_to',
        ),
        migrations.RemoveField(
            model_name='inspection',
            name='site',
        ),
        migrations.DeleteModel(
            name='Inspection',
        ),
        migrations.AlterModelOptions(
            name='hazard',
            options={'verbose_name': 'Hazard', 'verbose_name_plural': 'Hazards', 'permissions': (('browse_hazard', 'Can browse Hazard'), ('access_to_all_hazards', 'Has access to all Hazards'), ('access_to_pws_hazards', "Has access to PWS's Hazards"), ('change_all_info_about_hazard', 'Can change all information about Hazard'))},
        ),
        migrations.AlterModelOptions(
            name='site',
            options={'verbose_name': 'Site', 'verbose_name_plural': 'Sites', 'permissions': (('browse_site', 'Can browse Site'), ('access_to_all_sites', 'Has access to all Sites'), ('access_to_pws_sites', "Has access to PWS's Sites"), ('access_to_import', 'Can import Sites from Excel file'), ('access_to_batch_update', 'Has access to batch update'))},
        ),
        migrations.RemoveField(
            model_name='test',
            name='next_test_date',
        ),
    ]
