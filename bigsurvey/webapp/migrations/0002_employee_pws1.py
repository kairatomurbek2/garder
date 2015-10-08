# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_squashed_0050_delete_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='pws1',
            field=models.ManyToManyField(related_name='employees1', null=True, verbose_name='PWS', to='webapp.PWS', blank=True),
            preserve_default=True,
        ),
    ]