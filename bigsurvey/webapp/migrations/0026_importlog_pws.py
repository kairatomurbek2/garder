# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0025_importlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='importlog',
            name='pws',
            field=models.ForeignKey(to='webapp.PWS'),
            preserve_default=False,
        ),
    ]
