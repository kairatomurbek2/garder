# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_auto_20150302_0843'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='letter',
            name='customer',
        ),
        migrations.AddField(
            model_name='letter',
            name='site',
            field=models.ForeignKey(related_name='letters', verbose_name='Site', blank=True, to='webapp.Site', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pws',
            name='office_address',
            field=models.CharField(max_length=50, null=True, verbose_name='Office Address', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=15, null=True, verbose_name='Email', blank=True),
            preserve_default=True,
        ),
    ]
