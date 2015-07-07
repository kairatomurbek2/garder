# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0034_test_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='has_licence_for_installation',
            field=models.BooleanField(default=False, verbose_name='Determines whether tester has access for installation'),
            preserve_default=True,
        ),
    ]
