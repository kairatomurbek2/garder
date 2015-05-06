# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_auto_20150505_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='cv1_leaked',
            field=models.BooleanField(default=False, verbose_name='CV1 Leaked', choices=[(True, b'Leaked'), (False, b'Closed Tight')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='cv2_leaked',
            field=models.BooleanField(default=False, verbose_name='CV2 Leaked', choices=[(True, b'Leaked'), (False, b'Closed Tight')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='cv_leaked',
            field=models.BooleanField(default=False, verbose_name='CV Leaked', choices=[(True, b'Leaked'), (False, b'Closed Tight')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='outlet_sov_leaked',
            field=models.BooleanField(default=False, verbose_name='Outlet SOV Leaked', choices=[(True, b'Leaked'), (False, b'Closed Tight')]),
            preserve_default=True,
        ),
    ]
