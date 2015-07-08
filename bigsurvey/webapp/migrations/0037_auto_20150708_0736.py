# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0036_test_paypal_payment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='test_date',
            field=models.DateField(default=datetime.date.today, verbose_name='Test Date'),
            preserve_default=True,
        ),
    ]
