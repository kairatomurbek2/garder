# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0060_backup_backupbyowner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='backup',
            options={'verbose_name': 'Backup', 'verbose_name_plural': 'Backups', 'permissions': (('browse_backup', 'Can browse Backup'),)},
        ),
    ]
