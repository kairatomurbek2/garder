# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0029_merge'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='test',
            options={'ordering': ('-test_date', '-id'), 'verbose_name': 'Test', 'verbose_name_plural': 'Tests', 'permissions': (('browse_test', 'Can browse Test'), ('access_to_all_tests', 'Has access to all Tests'), ('access_to_pws_tests', "Has access to PWS's Tests"), ('access_to_own_tests', 'Has access to own Tests'))},
        ),
    ]
