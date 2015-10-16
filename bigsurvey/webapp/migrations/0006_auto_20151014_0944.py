# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_auto_20151008_0638'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'verbose_name': 'Employee', 'verbose_name_plural': 'Employees', 'permissions': (('browse_user', 'Can browse Users'), ('access_to_adminpanel', 'Can log into Admin Panel'), ('access_to_all_users', 'Has access to all Users'), ('access_to_pws_users', "Has access to PWS's Users"), ('access_to_multiple_pws_users', "Has access to Users from multiple PWS's"))},
        ),
    ]
