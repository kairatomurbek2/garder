# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('webapp', '0008_auto_20150305_0955'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statictext',
            name='key',
        ),
        migrations.AddField(
            model_name='statictext',
            name='group',
            field=models.ForeignKey(related_name='static_texts', verbose_name='Group', blank=True, to='auth.Group', null=True),
            preserve_default=True,
        ),
    ]
