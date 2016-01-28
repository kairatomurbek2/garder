# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0029_auto_20160127_0630'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestPriceHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.DecimalField(verbose_name='Price', max_digits=7, decimal_places=2)),
                ('start_date', models.DateField(auto_now_add=True, verbose_name='Start Date')),
                ('end_date', models.DateField(verbose_name='Price end date', null=True, editable=False, blank=True)),
            ],
            options={
                'verbose_name': 'Test Price',
                'verbose_name_plural': 'Test Price History',
                'permissions': (('setup_test_price', 'Can set up price per Test'),),
            },
            bases=(models.Model,),
        ),
    ]
