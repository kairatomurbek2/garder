# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_auto_20150505_0914'),
    ]

    operations = [
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('detail', models.CharField(max_length=100, verbose_name='Detail')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='test',
            name='cv1_cleaned',
            field=models.NullBooleanField(verbose_name='CV1 Cleaned or Replaced'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='cv1_replaced_details',
            field=models.ManyToManyField(related_name='cv1_replacements', to='webapp.Detail'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='cv2_cleaned',
            field=models.NullBooleanField(verbose_name='CV2 Cleaned or Replaced'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='cv2_replaced_details',
            field=models.ManyToManyField(related_name='cv2_replacements', to='webapp.Detail'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='pvb_cleaned',
            field=models.NullBooleanField(verbose_name='PVB Cleaned or Replaced'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='pvb_replaced_details',
            field=models.ManyToManyField(related_name='pvb_replacements', to='webapp.Detail'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='rv_cleaned',
            field=models.NullBooleanField(verbose_name='RV Cleaned or Replaced'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='rv_replaced_details',
            field=models.ManyToManyField(related_name='rv_replacements', to='webapp.Detail'),
            preserve_default=True,
        ),
    ]
