# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0020_auto_20150615_0714'),
    ]

    operations = [
        migrations.AddField(
            model_name='pws',
            name='logo',
            field=models.ImageField(upload_to=b'pws_logos', null=True, verbose_name='Pws logo', blank=True),
            preserve_default=True,
        ),
    ]
