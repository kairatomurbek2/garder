# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_auto_20150424_0933'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assemblylocation',
            options={'ordering': ('assembly_location',), 'verbose_name': 'Assembly Location', 'verbose_name_plural': 'Assembly Locations', 'permissions': (('browse_assemblylocation', 'Can browse Assembly Location'),)},
        ),
        migrations.AlterModelOptions(
            name='assemblystatus',
            options={'ordering': ('assembly_status',), 'verbose_name': 'Assembly Status', 'verbose_name_plural': 'Assembly Statuses', 'permissions': (('browse_assemblystatus', 'Can browse Assembly Status'),)},
        ),
        migrations.AlterModelOptions(
            name='bpmanufacturer',
            options={'ordering': ('bp_manufacturer',), 'verbose_name': 'BFP Manufacturer', 'verbose_name_plural': 'BFP Manufacturers', 'permissions': (('browse_bpmanufacturer', 'Can browse BP Manufacturer'),)},
        ),
        migrations.AlterModelOptions(
            name='bpsize',
            options={'ordering': ('bp_size',), 'verbose_name': 'BFP Size', 'verbose_name_plural': 'BFP Sizes', 'permissions': (('browse_bpsize', 'Can browse BP Size'),)},
        ),
        migrations.AlterModelOptions(
            name='bptype',
            options={'ordering': ('bp_type',), 'verbose_name': 'BFP Type', 'verbose_name_plural': 'BFP Types', 'permissions': (('browse_bptype', 'Can browse BP Type'),)},
        ),
        migrations.AlterModelOptions(
            name='customercode',
            options={'ordering': ('customer_code',), 'verbose_name': 'Customer Code', 'verbose_name_plural': 'Customer Codes', 'permissions': (('browse_customercode', 'Can browse Customer Code'),)},
        ),
        migrations.AlterModelOptions(
            name='floorscount',
            options={'ordering': ('floors_count',), 'verbose_name': 'Floors Count', 'verbose_name_plural': 'Floors Count', 'permissions': (('browse_floorscount', 'Can browse Floors Count'),)},
        ),
        migrations.AlterModelOptions(
            name='hazardtype',
            options={'ordering': ('hazard_type',), 'verbose_name': 'Hazard Type', 'verbose_name_plural': 'Hazard Types', 'permissions': (('browse_hazardtype', 'Can browse Hazard Type'),)},
        ),
        migrations.AlterModelOptions(
            name='icpointtype',
            options={'ordering': ('ic_point',), 'verbose_name': 'Interconnection Point Type', 'verbose_name_plural': 'Interconnection Point Types', 'permissions': (('browse_icpointtype', 'Can browse Interconnection Point Type'),)},
        ),
        migrations.AlterModelOptions(
            name='lettertype',
            options={'ordering': ('letter_type',), 'verbose_name': 'Letter Type', 'verbose_name_plural': 'Letter Types', 'permissions': (('browse_lettertype', 'Can browse Letter Type'),)},
        ),
        migrations.AlterModelOptions(
            name='orientation',
            options={'ordering': ('orientation',), 'verbose_name': 'Orientation Type', 'verbose_name_plural': 'Orientation Types', 'permissions': (('browse_orientation', 'Can browse Orientation Type'),)},
        ),
        migrations.AlterModelOptions(
            name='pws',
            options={'ordering': ('number',), 'verbose_name': 'Public Water System', 'verbose_name_plural': 'Public Water Systems', 'permissions': (('browse_pws', 'Can browse Public Water System'),)},
        ),
        migrations.AlterModelOptions(
            name='servicetype',
            options={'ordering': ('service_type',), 'verbose_name': 'Service Type', 'verbose_name_plural': 'Service Types', 'permissions': (('browse_servicetype', 'Can browse Service Type'),)},
        ),
        migrations.AlterModelOptions(
            name='sitestatus',
            options={'ordering': ('site_status',), 'verbose_name': 'Site Status', 'verbose_name_plural': 'Site Status', 'permissions': (('browse_sitestatus', 'Can browse Site Status'),)},
        ),
        migrations.AlterModelOptions(
            name='sitetype',
            options={'ordering': ('site_type',), 'verbose_name': 'Site Type', 'verbose_name_plural': 'Site Types', 'permissions': (('browse_sitetype', 'Can browse Site Type'),)},
        ),
        migrations.AlterModelOptions(
            name='siteuse',
            options={'ordering': ('site_use',), 'verbose_name': 'Site Use', 'verbose_name_plural': 'Site Use Types', 'permissions': (('browse_siteuse', 'Can browse Site Use'),)},
        ),
        migrations.AlterModelOptions(
            name='sourcetype',
            options={'ordering': ('source_type',), 'verbose_name': 'Source Type', 'verbose_name_plural': 'Source Types', 'permissions': (('browse_sourcetype', 'Can browse Source Type'),)},
        ),
        migrations.AlterModelOptions(
            name='special',
            options={'ordering': ('special',), 'verbose_name': 'Special', 'verbose_name_plural': 'Special', 'permissions': (('browse_special', 'Can browse Special'),)},
        ),
        migrations.AlterModelOptions(
            name='surveytype',
            options={'ordering': ('survey_type',), 'verbose_name': 'Survey Type', 'verbose_name_plural': 'Survey Types', 'permissions': (('browse_surveytype', 'Can browse Survey Type'),)},
        ),
        migrations.AlterModelOptions(
            name='testmanufacturer',
            options={'ordering': ('test_manufacturer',), 'verbose_name': 'Test Manufacturer', 'verbose_name_plural': 'Test Manufacturers', 'permissions': (('browse_testmanufacturer', 'Can browse Test Manufacturer'),)},
        ),
        migrations.AlterModelOptions(
            name='testmodel',
            options={'ordering': ('model',), 'verbose_name': 'Test Model', 'verbose_name_plural': 'Test Models', 'permissions': (('browse_testmodel', 'Can browse Test Models'),)},
        ),
    ]
