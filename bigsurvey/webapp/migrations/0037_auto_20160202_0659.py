# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0036_auto_20160202_0559'),
    ]

    operations = [
        migrations.CreateModel(
            name='DemoTrial',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateTimeField(null=True, verbose_name='Start Date', blank=True)),
                ('end_date', models.DateTimeField(null=True, verbose_name='End Date', blank=True)),
                ('employee', models.ForeignKey(related_name='demo_trials', verbose_name='Demo Trial Employee', blank=True, to='webapp.Employee', null=True)),
            ],
            options={
                'verbose_name': 'Demo Trial',
                'verbose_name_plural': 'Demo Trials',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='employee',
            name='has_paid',
            field=models.BooleanField(default=False, verbose_name='Has paid for demo trial'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pws',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='PWS is active'),
            preserve_default=True,
        ),
    ]
