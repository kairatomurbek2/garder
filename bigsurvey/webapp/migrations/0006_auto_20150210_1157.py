# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_auto_20150210_0816'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inspection',
            options={'verbose_name': 'Inspection', 'verbose_name_plural': 'Inspections', 'permissions': (('browse_inspection', 'Can browse Inspection'), ('access_to_all_inspections', 'Has access to all Inspections'), ('access_to_pws_inspections', 'Has access to PWS Inspections'))},
        ),
        migrations.AlterModelOptions(
            name='test',
            options={'verbose_name': 'Test', 'verbose_name_plural': 'Tests', 'permissions': (('browse_test', 'Can browse Test'), ('access_to_all_tests', 'Has access to all Tests'), ('access_to_pws_tests', "Has access to his PWS's Tests"), ('access_to_own_tests', 'Has access to his own Tests'), ('add_many_tests_per_hazard', 'Can add many Tests per Hazard'))},
        ),
        migrations.AlterModelOptions(
            name='testpermission',
            options={'verbose_name': 'Test Permission', 'verbose_name_plural': 'Test Permissions', 'permissions': (('browse_testpermission', 'Can browse Test Permission'), ('access_to_all_testpermissions', 'Has access to all Test Permissions'), ('access_to_pws_testpermissions', 'Has access to PWS Test Permissions'))},
        ),
        migrations.AlterField(
            model_name='test',
            name='tester',
            field=models.ForeignKey(related_name='tests', verbose_name='Tester', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
