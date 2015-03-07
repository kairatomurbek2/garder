# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testpermission',
            name='due_date',
        ),
        migrations.AddField(
            model_name='statictext',
            name='key',
            field=models.CharField(max_length=20, null=True, verbose_name='Key', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='statictext',
            name='text',
            field=models.TextField(null=True, verbose_name='Text', blank=True),
            preserve_default=True,
        ),
    ]
