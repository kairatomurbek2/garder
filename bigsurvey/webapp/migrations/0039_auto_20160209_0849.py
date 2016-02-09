# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0038_pws_county'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='code',
            field=models.CharField(default=uuid.uuid4, max_length=64, editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invite',
            name='invite_to',
            field=models.ForeignKey(related_name='invites_received', verbose_name='Invited user', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
