# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20150504_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='letter',
            name='hazard',
            field=models.ForeignKey(related_name='letters', verbose_name='Hazard', blank=True, to='webapp.Hazard', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='letter',
            name='rendered_body',
            field=models.TextField(null=True, verbose_name='Letter Content', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lettertype',
            name='template',
            field=ckeditor.fields.RichTextField(max_length=4000, null=True, verbose_name='Letter Template', blank=True),
            preserve_default=True,
        ),
    ]
