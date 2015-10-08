# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def copy_employees_from_foreign_to_m2m(apps, schema_editor):
    Employee = apps.get_model('webapp', 'Employee')
    for employee in Employee.objects.all():
        if employee.pws:
            employee.pws1.add(employee.pws)
            employee.save()


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_employee_pws1'),
    ]

    operations = [
        migrations.RunPython(copy_employees_from_foreign_to_m2m)
    ]
