# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0034_auto_20160201_0854'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testpricehistory',
            name='pws',
        ),
    ]
