# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_auto_20150505_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='contact_email',
            field=models.EmailField(max_length=30, null=True, verbose_name='Email', blank=True),
            preserve_default=True,
        ),
    ]
