# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pws',
            options={'verbose_name': 'Public Water System', 'verbose_name_plural': 'Public Water Systems', 'permissions': (('has_access_to_pws', 'Has access to PWS'),)},
        ),
        migrations.AlterModelOptions(
            name='site',
            options={'verbose_name': 'Site', 'verbose_name_plural': 'Sites', 'permissions': (('can_see_test_sites', 'Can see sites he has test permissions'), ('can_see_surv_sites', 'Can see sites assigned to him'), ('can_see_pws_sites', 'Can see sites belonging to his PWS'), ('can_see_all_sites', 'Can see all sites'))},
        ),
    ]
