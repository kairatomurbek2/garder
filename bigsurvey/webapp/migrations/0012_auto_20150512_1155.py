# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0011_auto_20150512_1132'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='site',
            unique_together=set([('pws', 'cust_number')]),
        ),
    ]
