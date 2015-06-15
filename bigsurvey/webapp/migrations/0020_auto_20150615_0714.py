# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0019_auto_20150612_0545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lettertype',
            name='pws',
            field=models.ForeignKey(related_name='letter_types', default=None, blank=True, to='webapp.PWS', null=True),
            preserve_default=True,
        ),
    ]
