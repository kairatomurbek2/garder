# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0056_auto_20160512_0440'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='site',
            unique_together=set([('pws', 'cust_number', 'address1', 'street_number', 'meter_number')]),
        ),
    ]
