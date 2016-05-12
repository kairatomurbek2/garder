# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0054_auto_20160310_0609'),
    ]

    operations = [
        migrations.AddField(
            model_name='importlog',
            name='duplicates_file',
            field=models.FileField(upload_to=b'excel_files/', null=True, verbose_name='Duplicate accounts file', blank=True),
            preserve_default=True,
        ),
    ]
