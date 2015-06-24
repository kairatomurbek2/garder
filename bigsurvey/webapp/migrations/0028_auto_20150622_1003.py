# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0027_auto_20150622_0928'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='importlog',
            options={'permissions': (('browse_import_log', 'Can browse Import Log'), ('access_to_all_import_logs', 'Has access to all Import Logs'), ('access_to_pws_import_logs', "Has access to PWS's Import Logs"))},
        ),
    ]
