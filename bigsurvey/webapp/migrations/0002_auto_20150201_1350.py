# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_squashed_0005_auto_20150130_1120'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activity_type', models.CharField(max_length=15, verbose_name='Site Status')),
            ],
            options={
                'verbose_name': 'Site Status',
                'verbose_name_plural': 'Site Status',
                'permissions': (('browse_site_status', 'Can browse Site Status'),),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='site',
            name='status',
            field=models.ForeignKey(related_name='sites', verbose_name='Status', blank=True, to='webapp.SiteStatus', null=True),
            preserve_default=True,
        ),
    ]
