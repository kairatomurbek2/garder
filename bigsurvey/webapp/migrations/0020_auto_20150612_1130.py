# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0019_auto_20150612_0857'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pws',
            name='consultant_number',
        ),
        migrations.AddField(
            model_name='pws',
            name='consultant_phone',
            field=models.CharField(max_length=50, null=True, verbose_name='Consultant Phone', blank=True),
            preserve_default=True,
        ),
    ]
