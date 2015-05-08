# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0008_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='address1',
            field=models.CharField(help_text='Main Address of Site', max_length=100, verbose_name='Address 1'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='address2',
            field=models.CharField(help_text='Secondary Address of Site if exists', max_length=100, null=True, verbose_name='Address 2', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='apt',
            field=models.CharField(help_text="Site Address's Apartment", max_length=15, null=True, verbose_name='Apt', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='city',
            field=models.CharField(help_text="Site's City", max_length=30, verbose_name='City'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='connect_date',
            field=models.DateField(help_text='Connection date of Site', null=True, verbose_name='Connect Date', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='contact_email',
            field=models.EmailField(help_text="Customer's Email Address", max_length=30, null=True, verbose_name='Email', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='contact_fax',
            field=models.CharField(help_text="Customer's Fax", max_length=15, null=True, verbose_name='Fax', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='contact_phone',
            field=models.CharField(help_text="Customer's Phone", max_length=15, null=True, verbose_name='Phone', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='cust_address1',
            field=models.CharField(help_text="Customer's Main Address", max_length=100, null=True, verbose_name='Address 1', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='cust_address2',
            field=models.CharField(help_text="Customer's Secondary Address (if exists)", max_length=100, null=True, verbose_name='Address 2', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='cust_apt',
            field=models.CharField(help_text="Customer's Apartment", max_length=15, null=True, verbose_name='Customer Apt', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='cust_city',
            field=models.CharField(help_text="Customer's City", max_length=30, null=True, verbose_name='City', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='cust_code',
            field=models.ForeignKey(related_name='customers', verbose_name='Customer Code', to='webapp.CustomerCode', help_text="Customer's Code"),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='cust_name',
            field=models.CharField(help_text="Customer's Name", max_length=50, verbose_name='Name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='cust_number',
            field=models.CharField(help_text="Customer's Number", max_length=15, verbose_name='Number'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='cust_state',
            field=models.CharField(choices=[(b'AL', b'Alabama'), (b'AK', b'Alaska'), (b'AZ', b'Arizona'), (b'AR', b'Arkansas'), (b'CA', b'California'), (b'CO', b'Colorado'), (b'CT', b'Connecticut'), (b'DE', b'Delaware'), (b'DC', b'District of Columbia'), (b'FL', b'Florida'), (b'GA', b'Georgia'), (b'HI', b'Hawaii'), (b'ID', b'Idaho'), (b'IL', b'Illinois'), (b'IN', b'Indiana'), (b'IA', b'Iowa'), (b'KS', b'Kansas'), (b'KY', b'Kentucky'), (b'LA', b'Louisiana'), (b'ME', b'Maine'), (b'MD', b'Maryland'), (b'MA', b'Massachusetts'), (b'MI', b'Michigan'), (b'MN', b'Minnesota'), (b'MS', b'Mississippi'), (b'MO', b'Missouri'), (b'MT', b'Montana'), (b'NE', b'Nebraska'), (b'NV', b'Nevada'), (b'NH', b'New Hampshire'), (b'NJ', b'New Jersey'), (b'NM', b'New Mexico'), (b'NY', b'New York'), (b'NC', b'North Carolina'), (b'ND', b'North Dakota'), (b'OH', b'Ohio'), (b'OK', b'Oklahoma'), (b'OR', b'Oregon'), (b'PA', b'Pennsylvania'), (b'RI', b'Rhode Island'), (b'SC', b'South Carolina'), (b'SD', b'South Dakota'), (b'TN', b'Tennessee'), (b'TX', b'Texas'), (b'UT', b'Utah'), (b'VT', b'Vermont'), (b'VA', b'Virginia'), (b'WA', b'Washington'), (b'WV', b'West Virginia'), (b'WI', b'Wisconsin'), (b'WY', b'Wyoming')], max_length=2, blank=True, help_text="Customer's State", null=True, verbose_name='State'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='cust_zip',
            field=models.CharField(help_text="Customer's ZIP Code", max_length=10, null=True, verbose_name='ZIP', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='fire_present',
            field=models.BooleanField(default=False, help_text='Is Fire connection present', verbose_name='Fire Present', choices=[(True, b'Yes'), (False, b'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='floors',
            field=models.ForeignKey(related_name='sites', blank=True, to='webapp.FloorsCount', help_text='Number of Floors', null=True, verbose_name='Building Height'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='interconnection_point',
            field=models.ForeignKey(related_name='sites', blank=True, to='webapp.ICPointType', help_text='Interconnection Point Type', null=True, verbose_name='Interconnection Point'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='irrigation_present',
            field=models.BooleanField(default=False, help_text='Is Irrigation connection present', verbose_name='Irrigation Present', choices=[(True, b'Yes'), (False, b'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='is_backflow',
            field=models.BooleanField(default=False, help_text='Is Backflow present', verbose_name='Is Backflow Present', choices=[(True, b'Yes'), (False, b'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='is_due_install',
            field=models.BooleanField(default=False, help_text='Is Due Install', verbose_name='Is Due Install', choices=[(True, b'Yes'), (False, b'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='last_survey_date',
            field=models.DateField(help_text='Last Survey Date', null=True, verbose_name='Last Survey Date', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='meter_number',
            field=models.CharField(help_text='Meter Number', max_length=20, null=True, verbose_name='Meter Number', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='meter_reading',
            field=models.FloatField(help_text='Meter Reading', null=True, verbose_name='Meter Reading', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='meter_size',
            field=models.CharField(help_text='Meter Size', max_length=15, null=True, verbose_name='Meter Size', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='next_survey_date',
            field=models.DateField(help_text='Next Survey Date', null=True, verbose_name='Next Survey Date', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='notes',
            field=models.TextField(help_text='Notes', max_length=255, null=True, verbose_name='Notes', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='potable_present',
            field=models.BooleanField(default=False, help_text='Is Potable connection present', verbose_name='Potable Present', choices=[(True, b'Yes'), (False, b'No')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='pws',
            field=models.ForeignKey(related_name='sites', verbose_name='PWS', to='webapp.PWS', help_text='PWS which Site belongs'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='route',
            field=models.CharField(help_text='Sequence Route', max_length=20, null=True, verbose_name='Seq. Route', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='site_type',
            field=models.ForeignKey(related_name='sites', blank=True, to='webapp.SiteType', help_text='Type of Site', null=True, verbose_name='Site Type'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='site_use',
            field=models.ForeignKey(related_name='sites', blank=True, to='webapp.SiteUse', help_text='Using of Site', null=True, verbose_name='Site Use'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='state',
            field=models.CharField(choices=[(b'AL', b'Alabama'), (b'AK', b'Alaska'), (b'AZ', b'Arizona'), (b'AR', b'Arkansas'), (b'CA', b'California'), (b'CO', b'Colorado'), (b'CT', b'Connecticut'), (b'DE', b'Delaware'), (b'DC', b'District of Columbia'), (b'FL', b'Florida'), (b'GA', b'Georgia'), (b'HI', b'Hawaii'), (b'ID', b'Idaho'), (b'IL', b'Illinois'), (b'IN', b'Indiana'), (b'IA', b'Iowa'), (b'KS', b'Kansas'), (b'KY', b'Kentucky'), (b'LA', b'Louisiana'), (b'ME', b'Maine'), (b'MD', b'Maryland'), (b'MA', b'Massachusetts'), (b'MI', b'Michigan'), (b'MN', b'Minnesota'), (b'MS', b'Mississippi'), (b'MO', b'Missouri'), (b'MT', b'Montana'), (b'NE', b'Nebraska'), (b'NV', b'Nevada'), (b'NH', b'New Hampshire'), (b'NJ', b'New Jersey'), (b'NM', b'New Mexico'), (b'NY', b'New York'), (b'NC', b'North Carolina'), (b'ND', b'North Dakota'), (b'OH', b'Ohio'), (b'OK', b'Oklahoma'), (b'OR', b'Oregon'), (b'PA', b'Pennsylvania'), (b'RI', b'Rhode Island'), (b'SC', b'South Carolina'), (b'SD', b'South Dakota'), (b'TN', b'Tennessee'), (b'TX', b'Texas'), (b'UT', b'Utah'), (b'VT', b'Vermont'), (b'VA', b'Virginia'), (b'WA', b'Washington'), (b'WV', b'West Virginia'), (b'WI', b'Wisconsin'), (b'WY', b'Wyoming')], max_length=2, blank=True, help_text="Site's State", null=True, verbose_name='State'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='status',
            field=models.ForeignKey(related_name='sites', blank=True, to='webapp.SiteStatus', help_text="Site's Status", null=True, verbose_name='Status'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='street_number',
            field=models.CharField(help_text="Site Address's Street Number", max_length=100, null=True, verbose_name='Street Number', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site',
            name='zip',
            field=models.CharField(help_text="Site's ZIP Code", max_length=10, null=True, verbose_name='ZIP', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='cv1_cleaned',
            field=models.BooleanField(default=True, verbose_name='CV1 Cleaned or Replaced', choices=[(True, b'Cleaned only'), (False, b'Replaced')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='cv1_replaced_details',
            field=models.ManyToManyField(related_name='cv1_replacements', null=True, to='webapp.Detail', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='cv2_cleaned',
            field=models.BooleanField(default=True, verbose_name='CV2 Cleaned or Replaced', choices=[(True, b'Cleaned only'), (False, b'Replaced')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='cv2_replaced_details',
            field=models.ManyToManyField(related_name='cv2_replacements', null=True, to='webapp.Detail', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='pvb_cleaned',
            field=models.BooleanField(default=True, verbose_name='PVB Cleaned or Replaced', choices=[(True, b'Cleaned only'), (False, b'Replaced')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='pvb_replaced_details',
            field=models.ManyToManyField(related_name='pvb_replacements', null=True, to='webapp.Detail', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='rv_cleaned',
            field=models.BooleanField(default=True, verbose_name='RV Cleaned or Replaced', choices=[(True, b'Cleaned only'), (False, b'Replaced')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='rv_replaced_details',
            field=models.ManyToManyField(related_name='rv_replacements', null=True, to='webapp.Detail', blank=True),
            preserve_default=True,
        ),
    ]
