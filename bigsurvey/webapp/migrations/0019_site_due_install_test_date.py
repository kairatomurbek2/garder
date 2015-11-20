# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0018_auto_20151119_0423'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='due_install_test_date',
            field=models.DateField(null=True, verbose_name='Due Test Date', blank=True),
            preserve_default=True,
        ),
    ]
