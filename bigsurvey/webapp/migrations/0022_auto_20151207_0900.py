# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0021_auto_20151204_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='address1',
            field=models.CharField(max_length=100, verbose_name='Service Street Address'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='address2',
            field=models.CharField(max_length=100, null=True, verbose_name='Service Secondary Address', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='apt',
            field=models.CharField(max_length=50, null=True, verbose_name='Service Apt', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='city',
            field=models.CharField(max_length=30, verbose_name='Service City'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='connect_date',
            field=models.DateField(null=True, verbose_name='Connect Date', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='contact_email',
            field=models.EmailField(max_length=30, null=True, verbose_name='Customer Email', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='contact_fax',
            field=models.CharField(max_length=15, null=True, verbose_name='Customer Fax', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='contact_phone',
            field=models.CharField(max_length=15, null=True, verbose_name='Customer Phone', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='cust_address1',
            field=models.CharField(max_length=100, null=True, verbose_name='Customer Main Address', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='cust_address2',
            field=models.CharField(max_length=100, null=True, verbose_name='Customer Secondary Address', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='cust_apt',
            field=models.CharField(max_length=50, null=True, verbose_name='Customer Apt', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='cust_city',
            field=models.CharField(max_length=30, null=True, verbose_name='Customer City', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='cust_code',
            field=models.ForeignKey(related_name='customers', verbose_name='Customer Code', to='webapp.CustomerCode'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='cust_name',
            field=models.CharField(max_length=50, verbose_name='Customer Name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='cust_number',
            field=models.CharField(max_length=15, verbose_name='Account Number', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='cust_state',
            field=models.CharField(blank=True, max_length=2, null=True, verbose_name='Customer State', choices=[(b'AL', b'Alabama'), (b'AK', b'Alaska'), (b'AZ', b'Arizona'), (b'AR', b'Arkansas'), (b'CA', b'California'), (b'CO', b'Colorado'), (b'CT', b'Connecticut'), (b'DE', b'Delaware'), (b'DC', b'District of Columbia'), (b'FL', b'Florida'), (b'GA', b'Georgia'), (b'HI', b'Hawaii'), (b'ID', b'Idaho'), (b'IL', b'Illinois'), (b'IN', b'Indiana'), (b'IA', b'Iowa'), (b'KS', b'Kansas'), (b'KY', b'Kentucky'), (b'LA', b'Louisiana'), (b'ME', b'Maine'), (b'MD', b'Maryland'), (b'MA', b'Massachusetts'), (b'MI', b'Michigan'), (b'MN', b'Minnesota'), (b'MS', b'Mississippi'), (b'MO', b'Missouri'), (b'MT', b'Montana'), (b'NE', b'Nebraska'), (b'NV', b'Nevada'), (b'NH', b'New Hampshire'), (b'NJ', b'New Jersey'), (b'NM', b'New Mexico'), (b'NY', b'New York'), (b'NC', b'North Carolina'), (b'ND', b'North Dakota'), (b'OH', b'Ohio'), (b'OK', b'Oklahoma'), (b'OR', b'Oregon'), (b'PA', b'Pennsylvania'), (b'RI', b'Rhode Island'), (b'SC', b'South Carolina'), (b'SD', b'South Dakota'), (b'TN', b'Tennessee'), (b'TX', b'Texas'), (b'UT', b'Utah'), (b'VT', b'Vermont'), (b'VA', b'Virginia'), (b'WA', b'Washington'), (b'WV', b'West Virginia'), (b'WI', b'Wisconsin'), (b'WY', b'Wyoming')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='cust_zip',
            field=models.CharField(max_length=10, null=True, verbose_name='Customer ZIP', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='fire_present',
            field=models.BooleanField(default=False, verbose_name='Fire Present', choices=[(True, b'Yes'), (False, b'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='floors',
            field=models.ForeignKey(related_name='sites', verbose_name='Number of Floors', blank=True, to='webapp.FloorsCount', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='interconnection_point',
            field=models.ForeignKey(related_name='sites', verbose_name='Interconnection Point', blank=True, to='webapp.ICPointType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='irrigation_present',
            field=models.BooleanField(default=False, verbose_name='Irrigation Present', choices=[(True, b'Yes'), (False, b'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='is_backflow',
            field=models.BooleanField(default=False, verbose_name='Is Backflow Present', choices=[(True, b'Yes'), (False, b'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='is_due_install',
            field=models.BooleanField(default=False, verbose_name='Is Due Install', choices=[(True, b'Yes'), (False, b'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='last_survey_date',
            field=models.DateField(null=True, verbose_name='Last Survey Date', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='meter_number',
            field=models.CharField(max_length=50, null=True, verbose_name='Meter Number', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='meter_reading',
            field=models.FloatField(null=True, verbose_name='Meter Reading', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='meter_size',
            field=models.CharField(max_length=50, null=True, verbose_name='Meter Size', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='next_survey_date',
            field=models.DateField(null=True, verbose_name='Next Survey Date', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='notes',
            field=models.TextField(max_length=255, null=True, verbose_name='Notes', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='potable_present',
            field=models.BooleanField(default=False, verbose_name='Potable Present', choices=[(True, b'Yes'), (False, b'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='pws',
            field=models.ForeignKey(related_name='sites', verbose_name='PWS', to='webapp.PWS'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='route',
            field=models.CharField(max_length=20, null=True, verbose_name='Sequence Route', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='site_type',
            field=models.ForeignKey(related_name='sites', verbose_name='Site Type', blank=True, to='webapp.SiteType', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='site_use',
            field=models.ForeignKey(related_name='sites', verbose_name='Site Use', blank=True, to='webapp.SiteUse', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='state',
            field=models.CharField(blank=True, max_length=2, null=True, verbose_name='Service State', choices=[(b'AL', b'Alabama'), (b'AK', b'Alaska'), (b'AZ', b'Arizona'), (b'AR', b'Arkansas'), (b'CA', b'California'), (b'CO', b'Colorado'), (b'CT', b'Connecticut'), (b'DE', b'Delaware'), (b'DC', b'District of Columbia'), (b'FL', b'Florida'), (b'GA', b'Georgia'), (b'HI', b'Hawaii'), (b'ID', b'Idaho'), (b'IL', b'Illinois'), (b'IN', b'Indiana'), (b'IA', b'Iowa'), (b'KS', b'Kansas'), (b'KY', b'Kentucky'), (b'LA', b'Louisiana'), (b'ME', b'Maine'), (b'MD', b'Maryland'), (b'MA', b'Massachusetts'), (b'MI', b'Michigan'), (b'MN', b'Minnesota'), (b'MS', b'Mississippi'), (b'MO', b'Missouri'), (b'MT', b'Montana'), (b'NE', b'Nebraska'), (b'NV', b'Nevada'), (b'NH', b'New Hampshire'), (b'NJ', b'New Jersey'), (b'NM', b'New Mexico'), (b'NY', b'New York'), (b'NC', b'North Carolina'), (b'ND', b'North Dakota'), (b'OH', b'Ohio'), (b'OK', b'Oklahoma'), (b'OR', b'Oregon'), (b'PA', b'Pennsylvania'), (b'RI', b'Rhode Island'), (b'SC', b'South Carolina'), (b'SD', b'South Dakota'), (b'TN', b'Tennessee'), (b'TX', b'Texas'), (b'UT', b'Utah'), (b'VT', b'Vermont'), (b'VA', b'Virginia'), (b'WA', b'Washington'), (b'WV', b'West Virginia'), (b'WI', b'Wisconsin'), (b'WY', b'Wyoming')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='status',
            field=models.ForeignKey(related_name='sites', verbose_name='Site Status', blank=True, to='webapp.SiteStatus', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='street_number',
            field=models.CharField(max_length=100, null=True, verbose_name='Service Street Number', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='zip',
            field=models.CharField(max_length=10, null=True, verbose_name='Service ZIP', blank=True),
            preserve_default=True,
        ),
    ]
