# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0044_auto_20150713_0929'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BPType',
        ),
    ]
