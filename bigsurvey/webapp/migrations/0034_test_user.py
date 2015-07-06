# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webapp', '0033_auto_20150702_0425'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='user',
            field=models.ForeignKey(related_name='added_tests', default=2, verbose_name='Who added test into System', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
