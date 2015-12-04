# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0019_site_due_install_test_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hazard',
            old_name='due_install_test_date',
            new_name='due_test_date',
        ),
    ]
