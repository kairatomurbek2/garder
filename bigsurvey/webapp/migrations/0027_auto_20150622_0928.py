# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0026_importlog_pws'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='importlog',
            options={'permissions': (('access_to_all_import_logs', 'Has access to all import logs'), ('access_to_pws_import_logs', "Has access to PWS's import logs"))},
        ),
    ]
