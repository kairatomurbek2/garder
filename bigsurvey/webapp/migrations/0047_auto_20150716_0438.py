# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0046_auto_20150715_1223'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='cv1_replaced_details',
        ),
        migrations.RemoveField(
            model_name='test',
            name='cv2_replaced_details',
        ),
        migrations.RemoveField(
            model_name='test',
            name='pvb_replaced_details',
        ),
        migrations.RemoveField(
            model_name='test',
            name='rv_replaced_details',
        ),
    ]
