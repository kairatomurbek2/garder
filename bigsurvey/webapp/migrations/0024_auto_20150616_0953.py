# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import webapp.fields


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0023_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pws',
            name='logo',
            field=webapp.fields.ImageField(upload_to=b'pws_logos', null=True, verbose_name='Pws logo', blank=True),
            preserve_default=True,
        ),
    ]
