# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssemblyLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('assembly_location', models.CharField(max_length=20, verbose_name='Assembly Location')),
            ],
            options={
                'verbose_name': 'Assembly Location',
                'verbose_name_plural': 'Assembly Locations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BPManufacturer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bp_manufacturer', models.CharField(max_length=30, verbose_name='BFP Manufacturer')),
            ],
            options={
                'verbose_name': 'BFP Manufacturer',
                'verbose_name_plural': 'BFP Manufacturers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BPSize',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bp_size', models.CharField(max_length=10, verbose_name='BFP Size')),
            ],
            options={
                'verbose_name': 'BFP Size',
                'verbose_name_plural': 'BFP Sizes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BPType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bp_type', models.CharField(max_length=10, verbose_name='BFP Type')),
            ],
            options={
                'verbose_name': 'BFP Type',
                'verbose_name_plural': 'BFP Types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=15, verbose_name='Number')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('address1', models.CharField(max_length=30, verbose_name='Address 1')),
                ('address2', models.CharField(max_length=30, null=True, verbose_name='Address 2', blank=True)),
                ('apt', models.CharField(max_length=15, null=True, verbose_name='Customer Apt', blank=True)),
                ('city', models.CharField(max_length=30, verbose_name='City')),
                ('state', models.CharField(max_length=2, verbose_name='State', choices=[(b'AL', b'Alabama'), (b'AK', b'Alaska'), (b'AZ', b'Arizona'), (b'AR', b'Arkansas'), (b'CA', b'California'), (b'CO', b'Colorado'), (b'CT', b'Connecticut'), (b'DE', b'Delaware'), (b'DC', b'District of Columbia'), (b'FL', b'Florida'), (b'GA', b'Georgia'), (b'HI', b'Hawaii'), (b'ID', b'Idaho'), (b'IL', b'Illinois'), (b'IN', b'Indiana'), (b'IA', b'Iowa'), (b'KS', b'Kansas'), (b'KY', b'Kentucky'), (b'LA', b'Louisiana'), (b'ME', b'Maine'), (b'MD', b'Maryland'), (b'MA', b'Massachusetts'), (b'MI', b'Michigan'), (b'MN', b'Minnesota'), (b'MS', b'Mississippi'), (b'MO', b'Missouri'), (b'MT', b'Montana'), (b'NE', b'Nebraska'), (b'NV', b'Nevada'), (b'NH', b'New Hampshire'), (b'NJ', b'New Jersey'), (b'NM', b'New Mexico'), (b'NY', b'New York'), (b'NC', b'North Carolina'), (b'ND', b'North Dakota'), (b'OH', b'Ohio'), (b'OK', b'Oklahoma'), (b'OR', b'Oregon'), (b'PA', b'Pennsylvania'), (b'RI', b'Rhode Island'), (b'SC', b'South Carolina'), (b'SD', b'South Dakota'), (b'TN', b'Tennessee'), (b'TX', b'Texas'), (b'UT', b'Utah'), (b'VT', b'Vermont'), (b'VA', b'Virginia'), (b'WA', b'Washington'), (b'WV', b'West Virginia'), (b'WI', b'Wisconsin'), (b'WY', b'Wyoming')])),
                ('zip', models.CharField(max_length=5, verbose_name='ZIP')),
                ('phone', models.CharField(max_length=10, null=True, verbose_name='Phone', blank=True)),
                ('notes', models.TextField(max_length=255, null=True, verbose_name='Notes', blank=True)),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CustomerCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('customer_code', models.CharField(max_length=20, verbose_name='Customer Code')),
            ],
            options={
                'verbose_name': 'Customer Code',
                'verbose_name_plural': 'Customer Codes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=50, verbose_name='Address')),
                ('city', models.CharField(max_length=30, verbose_name='City')),
                ('state', models.CharField(max_length=2, verbose_name='State', choices=[(b'AL', b'Alabama'), (b'AK', b'Alaska'), (b'AZ', b'Arizona'), (b'AR', b'Arkansas'), (b'CA', b'California'), (b'CO', b'Colorado'), (b'CT', b'Connecticut'), (b'DE', b'Delaware'), (b'DC', b'District of Columbia'), (b'FL', b'Florida'), (b'GA', b'Georgia'), (b'HI', b'Hawaii'), (b'ID', b'Idaho'), (b'IL', b'Illinois'), (b'IN', b'Indiana'), (b'IA', b'Iowa'), (b'KS', b'Kansas'), (b'KY', b'Kentucky'), (b'LA', b'Louisiana'), (b'ME', b'Maine'), (b'MD', b'Maryland'), (b'MA', b'Massachusetts'), (b'MI', b'Michigan'), (b'MN', b'Minnesota'), (b'MS', b'Mississippi'), (b'MO', b'Missouri'), (b'MT', b'Montana'), (b'NE', b'Nebraska'), (b'NV', b'Nevada'), (b'NH', b'New Hampshire'), (b'NJ', b'New Jersey'), (b'NM', b'New Mexico'), (b'NY', b'New York'), (b'NC', b'North Carolina'), (b'ND', b'North Dakota'), (b'OH', b'Ohio'), (b'OK', b'Oklahoma'), (b'OR', b'Oregon'), (b'PA', b'Pennsylvania'), (b'RI', b'Rhode Island'), (b'SC', b'South Carolina'), (b'SD', b'South Dakota'), (b'TN', b'Tennessee'), (b'TX', b'Texas'), (b'UT', b'Utah'), (b'VT', b'Vermont'), (b'VA', b'Virginia'), (b'WA', b'Washington'), (b'WV', b'West Virginia'), (b'WI', b'Wisconsin'), (b'WY', b'Wyoming')])),
                ('zip', models.CharField(max_length=10, verbose_name='ZIP')),
                ('company', models.CharField(max_length=30, verbose_name='Company')),
                ('phone1', models.CharField(max_length=20, verbose_name='Phone 1')),
                ('phone2', models.CharField(max_length=20, null=True, verbose_name='Phone 2', blank=True)),
                ('fax', models.CharField(max_length=20, null=True, verbose_name='Fax', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FloorsCount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('floors_count', models.CharField(max_length=10, verbose_name='Floors Count')),
            ],
            options={
                'verbose_name': 'Floors Count',
                'verbose_name_plural': 'Floors Count',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hazard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('BPPresent', models.BooleanField(default=False, verbose_name='Is BP Present', choices=[(True, b'Yes'), (False, b'No')])),
                ('assembly_status', models.BooleanField(default=False, verbose_name='Assembly Status', choices=[(True, b'Yes'), (False, b'No')])),
                ('installer', models.CharField(max_length=30, null=True, verbose_name='Installer', blank=True)),
                ('install_date', models.DateTimeField(null=True, verbose_name='Install Date', blank=True)),
                ('replace_date', models.DateField(null=True, verbose_name='Replace Date', blank=True)),
                ('model_no', models.CharField(max_length=15, null=True, verbose_name='BP Model No.', blank=True)),
                ('serial_no', models.CharField(max_length=15, null=True, verbose_name='BP Serial No.', blank=True)),
                ('due_install_test_date', models.DateField(null=True, verbose_name='Due Install/Test Date', blank=True)),
                ('notes', models.TextField(max_length=255, null=True, verbose_name='Notes', blank=True)),
                ('assembly_location', models.ForeignKey(verbose_name='Assembly Location', blank=True, to='webapp.AssemblyLocation', null=True)),
                ('bp_size', models.ForeignKey(verbose_name='BP Size', blank=True, to='webapp.BPSize', null=True)),
                ('bp_type_present', models.ForeignKey(related_name='bp_present', verbose_name='BP Type Present', blank=True, to='webapp.BPType', null=True)),
                ('bp_type_required', models.ForeignKey(related_name='bp_required', verbose_name='BP Type Required', blank=True, to='webapp.BPType', null=True)),
            ],
            options={
                'verbose_name': 'Hazard',
                'verbose_name_plural': 'Hazards',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HazardType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hazard_type', models.CharField(max_length=50, verbose_name='Hazard Type')),
            ],
            options={
                'verbose_name': 'Hazard Type',
                'verbose_name_plural': 'Hazard Types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ICPointType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ic_point', models.CharField(max_length=20, verbose_name='Interconnection Point')),
            ],
            options={
                'verbose_name': 'Interconnection Point Type',
                'verbose_name_plural': 'Interconnection Point Types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Inspection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('assigned_date', models.DateField(auto_now_add=True, verbose_name='Assigned Date')),
                ('notes', models.TextField(max_length=255, null=True, verbose_name='Notes', blank=True)),
                ('assigned_by', models.ForeignKey(related_name='assigner', verbose_name='Assigned By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('assigned_to', models.ForeignKey(related_name='surveyor', verbose_name='Assigned To', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Inspection',
                'verbose_name_plural': 'Inspections',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Send Date')),
            ],
            options={
                'verbose_name': 'Letter',
                'verbose_name_plural': 'Letters',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LetterType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('letter_type', models.CharField(max_length=20, verbose_name='Letter Type')),
                ('template', models.TextField(max_length=2000, null=True, verbose_name='Letter Template', blank=True)),
            ],
            options={
                'verbose_name': 'Letter Type',
                'verbose_name_plural': 'Letter Types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Licence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(verbose_name='End Date')),
                ('notes', models.TextField(max_length=255, null=True, verbose_name='Notes', blank=True)),
                ('given_by', models.ForeignKey(verbose_name='Given By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('given_to', models.ForeignKey(verbose_name='Given To', to='auth.Group')),
            ],
            options={
                'verbose_name': 'Licence',
                'verbose_name_plural': 'Licences',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Orientation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('orientation', models.CharField(max_length=15, verbose_name='Orientation')),
            ],
            options={
                'verbose_name': 'Orientation Type',
                'verbose_name_plural': 'Orientation Types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PWS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=15, verbose_name='Number')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('city', models.CharField(max_length=30, verbose_name='City')),
                ('notes', models.TextField(max_length=255, null=True, verbose_name='Notes', blank=True)),
            ],
            options={
                'verbose_name': 'Public Water System',
                'verbose_name_plural': 'Public Water Systems',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(max_length=255, null=True, verbose_name='Notes', blank=True)),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('service_type', models.CharField(max_length=20, verbose_name='Service Type')),
            ],
            options={
                'verbose_name': 'Service Type',
                'verbose_name_plural': 'Service Types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('connect_date', models.DateField(null=True, verbose_name='Connect Date', blank=True)),
                ('address', models.CharField(max_length=30, verbose_name='Address')),
                ('street_address', models.CharField(max_length=30, null=True, verbose_name='Street Address', blank=True)),
                ('street_number', models.CharField(max_length=10, null=True, verbose_name='Street Number', blank=True)),
                ('apt', models.CharField(max_length=15, null=True, verbose_name='Apt', blank=True)),
                ('city', models.CharField(max_length=30, verbose_name='City')),
                ('state', models.CharField(max_length=2, verbose_name='State', choices=[(b'AL', b'Alabama'), (b'AK', b'Alaska'), (b'AZ', b'Arizona'), (b'AR', b'Arkansas'), (b'CA', b'California'), (b'CO', b'Colorado'), (b'CT', b'Connecticut'), (b'DE', b'Delaware'), (b'DC', b'District of Columbia'), (b'FL', b'Florida'), (b'GA', b'Georgia'), (b'HI', b'Hawaii'), (b'ID', b'Idaho'), (b'IL', b'Illinois'), (b'IN', b'Indiana'), (b'IA', b'Iowa'), (b'KS', b'Kansas'), (b'KY', b'Kentucky'), (b'LA', b'Louisiana'), (b'ME', b'Maine'), (b'MD', b'Maryland'), (b'MA', b'Massachusetts'), (b'MI', b'Michigan'), (b'MN', b'Minnesota'), (b'MS', b'Mississippi'), (b'MO', b'Missouri'), (b'MT', b'Montana'), (b'NE', b'Nebraska'), (b'NV', b'Nevada'), (b'NH', b'New Hampshire'), (b'NJ', b'New Jersey'), (b'NM', b'New Mexico'), (b'NY', b'New York'), (b'NC', b'North Carolina'), (b'ND', b'North Dakota'), (b'OH', b'Ohio'), (b'OK', b'Oklahoma'), (b'OR', b'Oregon'), (b'PA', b'Pennsylvania'), (b'RI', b'Rhode Island'), (b'SC', b'South Carolina'), (b'SD', b'South Dakota'), (b'TN', b'Tennessee'), (b'TX', b'Texas'), (b'UT', b'Utah'), (b'VT', b'Vermont'), (b'VA', b'Virginia'), (b'WA', b'Washington'), (b'WV', b'West Virginia'), (b'WI', b'Wisconsin'), (b'WY', b'Wyoming')])),
                ('zip', models.CharField(max_length=10, verbose_name='ZIP')),
                ('potable_present', models.BooleanField(default=False, verbose_name='Potable Present', choices=[(True, b'Yes'), (False, b'No')])),
                ('fire_present', models.BooleanField(default=False, verbose_name='Fire Present', choices=[(True, b'Yes'), (False, b'No')])),
                ('irrigation_present', models.BooleanField(default=False, verbose_name='Irrigation Present', choices=[(True, b'Yes'), (False, b'No')])),
                ('is_due_install', models.BooleanField(default=False, verbose_name='Is Due Install', choices=[(True, b'Yes'), (False, b'No')])),
                ('is_backflow', models.BooleanField(default=False, verbose_name='Is Backflow Present', choices=[(True, b'Yes'), (False, b'No')])),
                ('next_survey_date', models.DateField(null=True, verbose_name='Next Survey Date', blank=True)),
                ('notes', models.TextField(max_length=255, null=True, verbose_name='Notes', blank=True)),
                ('PWS', models.ForeignKey(verbose_name='PWS', to='webapp.PWS')),
                ('customer', models.ForeignKey(verbose_name='Customer', to='webapp.Customer')),
                ('floors', models.ForeignKey(verbose_name='Building Height', to='webapp.FloorsCount')),
                ('interconnection_point', models.ForeignKey(verbose_name='Interconnection Point', to='webapp.ICPointType')),
            ],
            options={
                'verbose_name': 'Site',
                'verbose_name_plural': 'Sites',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SiteType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('site_type', models.CharField(max_length=50, verbose_name='Site Type')),
            ],
            options={
                'verbose_name': 'Site Type',
                'verbose_name_plural': 'Site Types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SiteUse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('site_use', models.CharField(max_length=20, verbose_name='Site Use')),
            ],
            options={
                'verbose_name': 'Site Use',
                'verbose_name_plural': 'Site Use Types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SourceType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source_type', models.CharField(max_length=50, verbose_name='Source Type')),
            ],
            options={
                'verbose_name': 'Source Type',
                'verbose_name_plural': 'Source Types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Special',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('special', models.CharField(max_length=5, verbose_name='Special')),
            ],
            options={
                'verbose_name': 'Special',
                'verbose_name_plural': 'Special',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('survey_date', models.DateTimeField(verbose_name='Survey Date')),
                ('metered', models.BooleanField(default=False, verbose_name='Metered', choices=[(True, b'Yes'), (False, b'No')])),
                ('meter_number', models.CharField(max_length=15, null=True, verbose_name='Meter Number', blank=True)),
                ('meter_size', models.CharField(max_length=15, null=True, verbose_name='Meter Size', blank=True)),
                ('meter_reading', models.FloatField(null=True, verbose_name='Meter Reading', blank=True)),
                ('pump_present', models.BooleanField(default=False, verbose_name='Pump Present', choices=[(True, b'Yes'), (False, b'No')])),
                ('additives_present', models.BooleanField(default=False, verbose_name='Additives Present', choices=[(True, b'Yes'), (False, b'No')])),
                ('cc_present', models.BooleanField(default=False, verbose_name='CC Present', choices=[(True, b'Yes'), (False, b'No')])),
                ('protected', models.BooleanField(default=False, verbose_name='Is Protected', choices=[(True, b'Yes'), (False, b'No')])),
                ('aux_water', models.BooleanField(default=False, verbose_name='Auxiliary Water', choices=[(True, b'Yes'), (False, b'No')])),
                ('detector_manufacturer', models.CharField(max_length=20, null=True, verbose_name='Detector Manufacturer', blank=True)),
                ('detector_model', models.CharField(max_length=20, null=True, verbose_name='Detector Model', blank=True)),
                ('detector_serial_no', models.CharField(max_length=20, null=True, verbose_name='Detector Serial No.', blank=True)),
                ('notes', models.TextField(max_length=255, null=True, verbose_name='Notes', blank=True)),
                ('service', models.ForeignKey(verbose_name='Service', to='webapp.Service')),
                ('special', models.ForeignKey(verbose_name='Special', blank=True, to='webapp.Special', null=True)),
            ],
            options={
                'verbose_name': 'Survey',
                'verbose_name_plural': 'Surveys',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SurveyType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('survey_type', models.CharField(max_length=20, verbose_name='Survey Type')),
            ],
            options={
                'verbose_name': 'Survey Type',
                'verbose_name_plural': 'Survey Types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('test_serial_number', models.CharField(max_length=20, verbose_name='Test Serial No.')),
                ('last_calibration_date', models.DateField(verbose_name='Last Calibration Date')),
                ('tester_certificate', models.CharField(max_length=15, verbose_name='Tester Certificate No.')),
                ('test_date', models.DateField(auto_now_add=True, verbose_name='Test Date')),
                ('next_test_date', models.DateField(null=True, verbose_name='Next Test Date', blank=True)),
                ('cv1_leaked', models.BooleanField(default=False, verbose_name='Leaked', choices=[(True, b'Leaked'), (False, b'Closed')])),
                ('cv1_gauge_pressure', models.FloatField(null=True, verbose_name='Gauge Pressure', blank=True)),
                ('cv1_maintenance', models.BooleanField(default=False, verbose_name='Maintenance', choices=[(True, b'Yes'), (False, b'No')])),
                ('cv1_maintenance_pressure', models.FloatField(null=True, verbose_name='Maintenance Pressure', blank=True)),
                ('cv2_leaked', models.BooleanField(default=False, verbose_name='Leaked', choices=[(True, b'Leaked'), (False, b'Closed')])),
                ('cv2_gauge_pressure', models.FloatField(null=True, verbose_name='Gauge Pressure', blank=True)),
                ('cv2_maintenance', models.BooleanField(default=False, verbose_name='Maintenance', choices=[(True, b'Yes'), (False, b'No')])),
                ('cv2_maintenance_pressure', models.FloatField(null=True, verbose_name='Maintenance Pressure', blank=True)),
                ('rv_opened', models.BooleanField(default=False, verbose_name='Opened', choices=[(True, b'Opened'), (False, b'Closed')])),
                ('rv_psi1', models.FloatField(null=True, verbose_name='Pressure 1', blank=True)),
                ('rv_psi2', models.FloatField(null=True, verbose_name='Pressure 2', blank=True)),
                ('rv_maintenance', models.BooleanField(default=False, verbose_name='Maintenance', choices=[(True, b'Yes'), (False, b'No')])),
                ('outlet_sov_leaked', models.BooleanField(default=False, verbose_name='Leaked', choices=[(True, b'Leaked'), (False, b'Closed')])),
                ('pvb_opened', models.BooleanField(default=False, verbose_name='PVB Opened', choices=[(True, b'Opened'), (False, b'Closed')])),
                ('pvb_open_pressure', models.FloatField(null=True, verbose_name='Open Pressure', blank=True)),
                ('cv_leaked', models.BooleanField(default=False, verbose_name='Leaked', choices=[(True, b'Leaked'), (False, b'Closed')])),
                ('cv_held_pressure', models.FloatField(null=True, verbose_name='Held Pressure', blank=True)),
                ('cv_maintenance', models.BooleanField(default=False, verbose_name='Maintenance', choices=[(True, b'Yes'), (False, b'No')])),
                ('air_inlet_psi', models.FloatField(null=True, verbose_name='Air Inlet PSI', blank=True)),
                ('cv_psi', models.FloatField(null=True, verbose_name='Check Valve PSI', blank=True)),
                ('test_result', models.BooleanField(default=False, verbose_name='Test Result', choices=[(True, b'Passed'), (False, b'Failed')])),
                ('notes', models.TextField(max_length=255, null=True, verbose_name='Notes', blank=True)),
                ('bp_device', models.ForeignKey(verbose_name='BP Device', to='webapp.Hazard')),
            ],
            options={
                'verbose_name': 'Test',
                'verbose_name_plural': 'Tests',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TestManufacturer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('test_manufacturer', models.CharField(max_length=20, verbose_name='Test Manufacturer')),
            ],
            options={
                'verbose_name': 'Test Manufacturer',
                'verbose_name_plural': 'Test Manufacturers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TestPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('given_date', models.DateField(auto_now_add=True, verbose_name='Given Date')),
                ('due_date', models.DateField(verbose_name='Due Date')),
                ('notes', models.TextField(max_length=255, null=True, verbose_name='Notes', blank=True)),
                ('given_by', models.ForeignKey(related_name='permitter', verbose_name='Given By', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('given_to', models.ForeignKey(related_name='tester', verbose_name='Given To', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Test Permission',
                'verbose_name_plural': 'Test Permissions',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='test',
            name='test_manufacturer',
            field=models.ForeignKey(verbose_name='Test Manufacturer', to='webapp.TestManufacturer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='tester',
            field=models.ForeignKey(verbose_name='Tester', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='survey',
            name='survey_type',
            field=models.ForeignKey(verbose_name='Survey Type', to='webapp.SurveyType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='survey',
            name='surveyor',
            field=models.ForeignKey(verbose_name='Surveyor', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='site',
            name='site_type',
            field=models.ForeignKey(verbose_name='Site Type', to='webapp.SiteType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='site',
            name='site_use',
            field=models.ForeignKey(verbose_name='Site Use', to='webapp.SiteUse'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='service',
            name='service_type',
            field=models.ForeignKey(verbose_name='Service Type', to='webapp.ServiceType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='service',
            name='site',
            field=models.ForeignKey(verbose_name='Site', to='webapp.Site'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pws',
            name='water_source',
            field=models.ForeignKey(verbose_name='Water Source', to='webapp.SourceType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='letter',
            name='letter_type',
            field=models.ForeignKey(verbose_name='Letter Type', to='webapp.LetterType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='letter',
            name='survey',
            field=models.ForeignKey(verbose_name='Survey', to='webapp.Survey'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='letter',
            name='user',
            field=models.ForeignKey(verbose_name='Sender', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inspection',
            name='site',
            field=models.ForeignKey(verbose_name='Site', to='webapp.Site'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hazard',
            name='hazard_type',
            field=models.ForeignKey(verbose_name='Hazard Type', to='webapp.HazardType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hazard',
            name='manufacturer',
            field=models.ForeignKey(verbose_name='BP Manufacturer', blank=True, to='webapp.BPManufacturer', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hazard',
            name='orientation',
            field=models.ForeignKey(verbose_name='orientation', blank=True, to='webapp.Orientation', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hazard',
            name='survey',
            field=models.ForeignKey(verbose_name='Survey', to='webapp.Survey'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='code',
            field=models.ForeignKey(verbose_name='Customer Code', to='webapp.CustomerCode'),
            preserve_default=True,
        ),
    ]
