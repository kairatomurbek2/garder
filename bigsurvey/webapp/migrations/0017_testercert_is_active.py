# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0016_auto_20151110_1022'),
    ]

    operations = [
        migrations.AddField(
            model_name='testercert',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Is still valid'),
            preserve_default=True,
        ),
    ]
