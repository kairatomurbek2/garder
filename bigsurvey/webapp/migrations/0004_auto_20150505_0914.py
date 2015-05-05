# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20150505_0905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lettertype',
            name='template',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='Letter Template', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='statictext',
            name='text',
            field=ckeditor.fields.RichTextField(null=True, verbose_name='Text', blank=True),
            preserve_default=True,
        ),
    ]
