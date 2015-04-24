# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_site_street_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='site',
            options={'verbose_name': 'Site', 'verbose_name_plural': 'Sites', 'permissions': (('browse_site', 'Can browse Site'), ('access_to_all_sites', 'Has access to all Sites'), ('access_to_pws_sites', "Has access to PWS's Sites"), ('access_to_import', 'Can import Sites from Excel file'), ('access_to_batch_update', 'Has access to batch update'), ('change_all_info_about_site', 'Can change all information about Site'))},
        ),
    ]
