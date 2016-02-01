# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0032_auto_20160129_0516'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statictext',
            name='text',
        ),
        migrations.RemoveField(
            model_name='statictext',
            name='title',
        ),
        migrations.AddField(
            model_name='statictext',
            name='pdf_file',
            field=models.FileField(default=None, upload_to=b'help', verbose_name='Help File'),
            preserve_default=True,
        ),
    ]
