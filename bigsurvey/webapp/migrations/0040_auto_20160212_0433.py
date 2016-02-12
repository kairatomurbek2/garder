# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0039_auto_20160211_0853'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.DecimalField(default=Decimal('5'), verbose_name='Price', max_digits=7, decimal_places=2)),
                ('start_date', models.DateField(auto_now_add=True, verbose_name='Start Date')),
                ('end_date', models.DateField(verbose_name='Price end date', null=True, editable=False, blank=True)),
                ('price_type', models.CharField(default=b'demo_trial_price', max_length=50, choices=[(b'demo_trial_price', 'Demo Trial Price'), (b'test_price', 'Test Price')])),
            ],
            options={
                'verbose_name': 'Price',
                'verbose_name_plural': 'Price History',
                'permissions': (('setup_test_price', 'Can set up price'),),
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='TestPriceHistory',
        ),
        migrations.AlterField(
            model_name='employee',
            name='user',
            field=models.OneToOneField(related_name='employee', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
