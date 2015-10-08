# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20151008_0628'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='pws',
        ),
        migrations.AlterField(
            model_name='employee',
            name='pws1',
            field=models.ManyToManyField(related_name='employees', null=True, verbose_name='PWS', to='webapp.PWS', blank=True),
            preserve_default=True,
        ),
    ]
