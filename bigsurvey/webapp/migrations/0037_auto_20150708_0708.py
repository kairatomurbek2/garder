# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0036_test_paypal_payment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='hazard',
            name='additives_present',
            field=models.BooleanField(default=False, verbose_name='Additives Present', choices=[(True, b'Yes'), (False, b'No')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hazard',
            name='aux_water',
            field=models.BooleanField(default=False, verbose_name='Auxiliary Water', choices=[(True, b'Yes'), (False, b'No')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hazard',
            name='cc_present',
            field=models.BooleanField(default=False, verbose_name='CC Present', choices=[(True, b'Yes'), (False, b'No')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hazard',
            name='pump_present',
            field=models.BooleanField(default=False, verbose_name='Pump Present', choices=[(True, b'Yes'), (False, b'No')]),
            preserve_default=True,
        ),
    ]
