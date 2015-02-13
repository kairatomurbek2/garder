# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_auto_20150210_1157'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'verbose_name': 'Employee', 'verbose_name_plural': 'Employees', 'permissions': (('browse_user', 'Can browse Users'), ('access_to_adminpanel', 'Can log into Admin Panel'), ('access_to_all_users', 'Has access to all Users'), ('access_to_pws_users', 'Has access to PWS Users'))},
        ),
    ]
