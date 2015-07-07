# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0035_employee_has_licence_for_installation'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='paypal_payment_id',
            field=models.CharField(max_length=50, null=True, verbose_name='Paypal Payment ID', blank=True),
            preserve_default=True,
        ),
    ]
