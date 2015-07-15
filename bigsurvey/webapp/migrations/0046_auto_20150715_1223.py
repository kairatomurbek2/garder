# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0045_delete_bptype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hazard',
            name='bp_type_present',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='BP Type Present', choices=[('Air Gap', 'Air Gap'), ('AVB', 'AVB'), ('DC', 'DC'), ('DCDA', 'DCDA'), ('HBVB', 'HBVB'), ('PVB', 'PVB'), ('RP', 'RP'), ('RPDA', 'RPDA'), ('SVB', 'SVB')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hazard',
            name='bp_type_required',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='BP Type Required', choices=[('Air Gap', 'Air Gap'), ('AVB', 'AVB'), ('DC', 'DC'), ('DCDA', 'DCDA'), ('HBVB', 'HBVB'), ('PVB', 'PVB'), ('RP', 'RP'), ('RPDA', 'RPDA'), ('SVB', 'SVB')]),
            preserve_default=True,
        ),
    ]
