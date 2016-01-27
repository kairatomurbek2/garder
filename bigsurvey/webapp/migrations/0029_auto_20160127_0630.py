# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0028_survey_letter_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bpdevice',
            name='bp_type_present',
            field=models.CharField(max_length=15, verbose_name='BP Type Present', choices=[(b'Air Gap', b'Air Gap'), (b'AVB', b'AVB'), (b'DC', b'DC'), (b'DCDA', b'DCDA'), (b'HBVB', b'HBVB'), (b'PVB', b'PVB'), (b'RP', b'RP'), (b'RPDA', b'RPDA'), (b'SVB', b'SVB'), (b'Unknown', b'Unknown')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hazard',
            name='bp_type_required',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='BP Type Required', choices=[(b'Air Gap', b'Air Gap'), (b'AVB', b'AVB'), (b'DC', b'DC'), (b'DCDA', b'DCDA'), (b'HBVB', b'HBVB'), (b'PVB', b'PVB'), (b'RP', b'RP'), (b'RPDA', b'RPDA'), (b'SVB', b'SVB'), (b'Unknown', b'Unknown')]),
            preserve_default=True,
        ),
    ]
