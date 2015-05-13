# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import webapp.utils.photo_util


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0010_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Regulation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='Regulation Type')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Regulation Type',
                'verbose_name_plural': 'Regulation Types',
                'permissions': ('browse_regulation', 'Can browse Regulation Type'),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='hazard',
            name='latitude',
            field=models.FloatField(default=0, null=True, verbose_name='Latitude', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hazard',
            name='longitude',
            field=models.FloatField(default=0, null=True, verbose_name='Longitude', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hazard',
            name='photo',
            field=models.ImageField(default=None, upload_to=webapp.utils.photo_util.rename, null=True, verbose_name='Photo', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hazard',
            name='photo_thumb',
            field=models.ImageField(default=None, upload_to=b'photo/thumb/', null=True, verbose_name='Photo Thumbnail', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hazard',
            name='regulation_type',
            field=models.ForeignKey(related_name='hazards', verbose_name='Regulation', blank=True, to='webapp.Regulation', null=True),
            preserve_default=True,
        ),
    ]
