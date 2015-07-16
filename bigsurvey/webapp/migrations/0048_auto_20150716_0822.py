# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0047_auto_20150716_0438'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='licence',
            name='given_by',
        ),
        migrations.RemoveField(
            model_name='licence',
            name='given_to',
        ),
        migrations.DeleteModel(
            name='Licence',
        ),
        migrations.AlterModelOptions(
            name='importlog',
            options={'verbose_name': 'Import Log', 'verbose_name_plural': 'Import Logs', 'permissions': (('browse_import_log', 'Can browse Import Log'), ('access_to_all_import_logs', 'Has access to all Import Logs'), ('access_to_pws_import_logs', "Has access to PWS's Import Logs"))},
        ),
        migrations.AlterModelOptions(
            name='statictext',
            options={'verbose_name': 'Static Text', 'verbose_name_plural': 'Static Texts'},
        ),
        migrations.AlterField(
            model_name='importlog',
            name='added_sites',
            field=models.ManyToManyField(related_name='added_imports', verbose_name='Added sites', to='webapp.Site'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='importlog',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Datetime of import'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='importlog',
            name='deactivated_sites',
            field=models.ManyToManyField(related_name='deactivated_imports', verbose_name='Deactivated sites', to='webapp.Site'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='importlog',
            name='progress',
            field=models.IntegerField(default=0, verbose_name='Progress of import'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='importlog',
            name='pws',
            field=models.ForeignKey(related_name='import_logs', verbose_name='PWS for which import was performed', to='webapp.PWS'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='importlog',
            name='updated_sites',
            field=models.ManyToManyField(related_name='updated_imports', verbose_name='Updated sites', to='webapp.Site'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='importlog',
            name='user',
            field=models.ForeignKey(related_name='import_logs', verbose_name='User who performed import', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
