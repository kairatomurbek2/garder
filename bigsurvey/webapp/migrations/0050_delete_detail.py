# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0049_auto_20150716_1107'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Detail',
        ),
    ]
