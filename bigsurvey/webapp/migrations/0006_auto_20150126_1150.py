# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_auto_20150121_1107'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='service_type',
        ),
        migrations.RemoveField(
            model_name='service',
            name='site',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='service',
        ),
        migrations.DeleteModel(
            name='Service',
        ),
        migrations.AddField(
            model_name='survey',
            name='service_type',
            field=models.ForeignKey(related_name='surveys', default=1, verbose_name='Service Type', to='webapp.ServiceType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='survey',
            name='site',
            field=models.ForeignKey(related_name='surveys', default=1, verbose_name='Site', to='webapp.Site'),
            preserve_default=False,
        ),
    ]
