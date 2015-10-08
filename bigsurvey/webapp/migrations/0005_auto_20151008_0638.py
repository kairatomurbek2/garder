# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_auto_20151008_0638'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='pws1',
            new_name='pws',
        ),
    ]
