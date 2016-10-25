# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0063_auto_20161021_0440'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bpdevice',
            name='due_test_date',
        ),
        migrations.RemoveField(
            model_name='hazard',
            name='due_install_date',
        ),
    ]
