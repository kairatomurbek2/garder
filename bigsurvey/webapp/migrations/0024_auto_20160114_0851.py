# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0023_auto_20160113_0920'),
    ]

    operations = [
        migrations.CreateModel(
            name='BPDevice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('installed_properly', models.BooleanField(default=False, verbose_name='Installed Properly', choices=[(True, b'Yes'), (False, b'No')])),
                ('installer', models.CharField(max_length=30, null=True, verbose_name='Installer', blank=True)),
                ('install_date', models.DateField(null=True, verbose_name='Install Date', blank=True)),
                ('replace_date', models.DateField(null=True, verbose_name='Replace Date', blank=True)),
                ('bp_type_present', models.CharField(blank=True, max_length=15, null=True, verbose_name='BP Type Present', choices=[(b'Air Gap', b'Air Gap'), (b'AVB', b'AVB'), (b'DC', b'DC'), (b'DCDA', b'DCDA'), (b'HBVB', b'HBVB'), (b'PVB', b'PVB'), (b'RP', b'RP'), (b'RPDA', b'RPDA'), (b'SVB', b'SVB')])),
                ('model_no', models.CharField(max_length=30, null=True, verbose_name='BP Model No.', blank=True)),
                ('serial_no', models.CharField(max_length=30, null=True, verbose_name='BP Serial No.', blank=True)),
                ('due_test_date', models.DateField(null=True, verbose_name='Due Install/Test Date', blank=True)),
                ('notes', models.TextField(max_length=255, null=True, verbose_name='Notes', blank=True)),
                ('assembly_location', models.ForeignKey(related_name='hazards', verbose_name='Assembly Location', blank=True, to='webapp.AssemblyLocation', null=True)),
                ('bp_size', models.ForeignKey(related_name='hazards', verbose_name='BP Size', blank=True, to='webapp.BPSize', null=True)),
                ('manufacturer', models.ForeignKey(related_name='hazards', verbose_name='BP Manufacturer', blank=True, to='webapp.BPManufacturer', null=True)),
                ('orientation', models.ForeignKey(related_name='hazards', verbose_name='orientation', blank=True, to='webapp.Orientation', null=True)),
            ],
            options={
                'verbose_name': 'BP Device',
                'verbose_name_plural': 'BP Devices',
                'permissions': (('browse_devices', 'Can browse BP Device'), ('access_to_all_devices', 'Has access to all BP Devices'), ('access_to_pws_devices', "Has access to PWS's BP Devices"), ('access_to_multiple_pws_devices', "Has access to multiple PWS' BP Devices")),
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='hazard',
            options={'verbose_name': 'Hazard', 'verbose_name_plural': 'Hazards', 'permissions': (('browse_hazard', 'Can browse Hazard'), ('access_to_all_hazards', 'Has access to all Hazards'), ('access_to_pws_hazards', "Has access to PWS's Hazards"), ('access_to_multiple_pws_hazards', "Has access to multiple PWS' Hazards"))},
        ),
        migrations.RemoveField(
            model_name='hazard',
            name='assembly_location',
        ),
        migrations.RemoveField(
            model_name='hazard',
            name='bp_size',
        ),
        migrations.RemoveField(
            model_name='hazard',
            name='bp_type_present',
        ),
        migrations.RemoveField(
            model_name='hazard',
            name='due_test_date',
        ),
        migrations.RemoveField(
            model_name='hazard',
            name='install_date',
        ),
        migrations.RemoveField(
            model_name='hazard',
            name='installed_properly',
        ),
        migrations.RemoveField(
            model_name='hazard',
            name='installer',
        ),
        migrations.RemoveField(
            model_name='hazard',
            name='manufacturer',
        ),
        migrations.RemoveField(
            model_name='hazard',
            name='model_no',
        ),
        migrations.RemoveField(
            model_name='hazard',
            name='orientation',
        ),
        migrations.RemoveField(
            model_name='hazard',
            name='replace_date',
        ),
        migrations.RemoveField(
            model_name='hazard',
            name='serial_no',
        ),
        migrations.AddField(
            model_name='hazard',
            name='bp_device',
            field=models.OneToOneField(related_name='hazard', null=True, blank=True, to='webapp.BPDevice'),
            preserve_default=True,
        ),
    ]
