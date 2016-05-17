# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import webapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0057_auto_20160513_0216'),
    ]

    operations = [
        migrations.CreateModel(
            name='TermsConditions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pdf_file', models.FileField(default=None, upload_to=b'media', verbose_name='PDF File', validators=[webapp.models.validate_file_is_pdf])),
            ],
            options={
                'verbose_name': 'Term and Condition',
                'verbose_name_plural': 'Terms and Conditions',
            },
            bases=(models.Model,),
        ),
    ]
