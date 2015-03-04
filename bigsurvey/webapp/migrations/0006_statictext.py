# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_auto_20150303_1237'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaticText',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=20, verbose_name='Title')),
                ('text', redactor.fields.RedactorField(null=True, verbose_name='Text', blank=True)),
            ],
            options={
                'verbose_name': 'Static Text',
                'verbose_name_plural': 'Static Text',
            },
            bases=(models.Model,),
        ),
    ]
