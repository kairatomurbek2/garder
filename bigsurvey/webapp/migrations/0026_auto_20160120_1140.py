# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0025_auto_20160120_0602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hazard',
            name='assembly_status',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Assembly Status', choices=[(b'installed', 'Installed'), (b'due_install', 'Due Install'), (b'due_replace', 'Due Replace'), (b'maintenance', 'Maintenance'), (b'not_required', 'Not Required')]),
            preserve_default=True,
        ),
    ]
