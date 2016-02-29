# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations
from django.contrib.contenttypes.management import update_contenttypes
from django.apps import apps as configured_apps
from django.contrib.auth.management import create_permissions

PERMISSIONS_TO_ADD = [
    'browse_hazard_list',

]

GROUPS_TO_ADD = [
    'Administrative Authority',
    'Administrators',
    'PWSOwners',
    'SuperAdministrators',
    'Surveyors'

]


class Migration(migrations.Migration):
    def add_permission(apps, schema_editor):
        for app in configured_apps.get_app_configs():
            update_contenttypes(app, interactive=True, verbosity=0)

        for app in configured_apps.get_app_configs():
            create_permissions(app, verbosity=0)

        Group = apps.get_model('auth', 'Group')
        Permission = apps.get_model('auth', 'Permission')
        for group_name in GROUPS_TO_ADD:
            try:
                group = Group.objects.get(name=group_name)
                permissions = [Permission.objects.get(codename=i) for i in PERMISSIONS_TO_ADD]
                group.permissions.add(*permissions)
            except Group.DoesNotExist:
                pass


    dependencies = [
        ('webapp', '0040_auto_20160212_0433'),
    ]

    operations = [
        migrations.RunPython(add_permission),
    ]
