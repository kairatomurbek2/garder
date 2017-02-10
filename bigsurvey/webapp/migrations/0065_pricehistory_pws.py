# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0064_auto_20161021_0515'),
    ]

    operations = [
        migrations.AddField(
            model_name='pricehistory',
            name='pws',
            field=models.ForeignKey(verbose_name='PWS', blank=True, to='webapp.PWS', null=True),
            preserve_default=True,
        ),
    ]
