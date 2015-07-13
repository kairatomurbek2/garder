# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0042_pws_state'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pws',
            options={'ordering': ('number',), 'verbose_name': 'Public Water System', 'verbose_name_plural': 'Public Water Systems', 'permissions': (('browse_pws', 'Can browse Public Water System'), ('browse_all_pws', 'Can browse all Public Water Systems'), ('change_own_pws', 'Can change his own Public Water System'))},
        ),
    ]
