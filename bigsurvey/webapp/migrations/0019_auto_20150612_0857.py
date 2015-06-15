# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0018_auto_20150609_0648'),
    ]

    operations = [
        migrations.AddField(
            model_name='pws',
            name='consultant_name',
            field=models.CharField(max_length=100, null=True, verbose_name='Consultant Name', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pws',
            name='consultant_number',
            field=models.CharField(max_length=50, null=True, verbose_name='Consultant Number', blank=True),
            preserve_default=True,
        ),
    ]
