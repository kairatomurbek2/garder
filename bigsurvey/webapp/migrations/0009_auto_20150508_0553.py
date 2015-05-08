# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0008_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='lettertype',
            name='header',
            field=models.CharField(default='Backflow Prevention Services Notification', max_length=150, verbose_name='Letter Header'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lettertype',
            name='template',
            field=ckeditor.fields.RichTextField(default='Default Letter Template', verbose_name='Letter Template'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='cv1_cleaned',
            field=models.BooleanField(default=True, verbose_name='CV1 Cleaned or Replaced', choices=[(True, b'Cleaned only'), (False, b'Replaced')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='cv1_replaced_details',
            field=models.ManyToManyField(related_name='cv1_replacements', null=True, to='webapp.Detail', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='cv2_cleaned',
            field=models.BooleanField(default=True, verbose_name='CV2 Cleaned or Replaced', choices=[(True, b'Cleaned only'), (False, b'Replaced')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='cv2_replaced_details',
            field=models.ManyToManyField(related_name='cv2_replacements', null=True, to='webapp.Detail', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='pvb_cleaned',
            field=models.BooleanField(default=True, verbose_name='PVB Cleaned or Replaced', choices=[(True, b'Cleaned only'), (False, b'Replaced')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='pvb_replaced_details',
            field=models.ManyToManyField(related_name='pvb_replacements', null=True, to='webapp.Detail', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='rv_cleaned',
            field=models.BooleanField(default=True, verbose_name='RV Cleaned or Replaced', choices=[(True, b'Cleaned only'), (False, b'Replaced')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='rv_replaced_details',
            field=models.ManyToManyField(related_name='rv_replacements', null=True, to='webapp.Detail', blank=True),
            preserve_default=True,
        ),
    ]
