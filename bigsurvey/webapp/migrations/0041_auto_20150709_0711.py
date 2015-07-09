# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0040_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='pws',
            name='bailee_job_title',
            field=models.CharField(default=b'Director of Public Works', max_length=100, verbose_name='Job title of person on whose behalf the letter will be sent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pws',
            name='bailee_name',
            field=models.CharField(max_length=100, null=True, verbose_name='Name of Director of Public Works or other person on whose behalf the letter will be sent', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pws',
            name='email',
            field=models.EmailField(max_length=100, null=True, verbose_name="PWS's email", blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pws',
            name='fax',
            field=models.CharField(max_length=100, null=True, verbose_name="PWS's Fax number", blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pws',
            name='letter_left_header_block',
            field=ckeditor.fields.RichTextField(verbose_name='Letter Left Header block', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pws',
            name='letter_right_header_block',
            field=ckeditor.fields.RichTextField(verbose_name='Letter Right Header block', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pws',
            name='phone',
            field=models.CharField(max_length=100, null=True, verbose_name="PWS's Phone number", blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pws',
            name='zip',
            field=models.CharField(max_length=10, null=True, verbose_name='ZIP', blank=True),
            preserve_default=True,
        ),
    ]
