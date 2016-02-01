# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import webapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0033_auto_20160201_0844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statictext',
            name='pdf_file',
            field=models.FileField(default=None, upload_to=b'help', verbose_name='Help File', validators=[webapp.models.validate_file_is_pdf]),
            preserve_default=True,
        ),
    ]
