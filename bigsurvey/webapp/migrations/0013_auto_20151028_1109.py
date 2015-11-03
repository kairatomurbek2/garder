# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0012_auto_20151027_0614'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='test_last_cert',
            field=models.DateField(null=True, verbose_name='Last Cert.', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='test_manufacturer',
            field=models.ForeignKey(related_name='tests', verbose_name='Test Manufacturer', blank=True, to='webapp.TestManufacturer', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='test_model',
            field=models.ForeignKey(related_name='tests', verbose_name='Test Model', blank=True, to='webapp.TestModel', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='test_serial',
            field=models.CharField(max_length=20, null=True, verbose_name='Test Serial', blank=True),
            preserve_default=True,
        ),
    ]
