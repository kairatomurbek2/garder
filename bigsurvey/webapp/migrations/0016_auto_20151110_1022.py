# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webapp', '0015_auto_20151109_1031'),
    ]

    operations = [
        migrations.CreateModel(
            name='HazardDegree',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('degree', models.CharField(max_length=50, verbose_name='Hazard Degree')),
            ],
            options={
                'ordering': ('pk',),
                'verbose_name': 'Hazard Degree',
                'verbose_name_plural': 'Hazard Degrees',
                'permissions': (('browse_hazard_degree', 'Can browse Hazard Degree'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TesterCert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cert_number', models.CharField(max_length=30, verbose_name='Cert. Number')),
                ('cert_date', models.DateField(null=True, verbose_name='Cert. Date', blank=True)),
                ('cert_expires', models.DateField(null=True, verbose_name='Cert. Expires', blank=True)),
                ('user', models.ForeignKey(related_name='certs', verbose_name='Owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Tester Certificate',
                'verbose_name_plural': 'Tester Certificates',
                'permissions': (('access_to_all_tester_certs', "Access to all testers' certs"), ('access_to_pws_tester_certs', "Access to own PWS' testers' certs")),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TestKit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('test_serial', models.CharField(max_length=20, verbose_name='Test Serial')),
                ('test_last_cert', models.DateField(null=True, verbose_name='Last Cert.', blank=True)),
                ('test_manufacturer', models.ForeignKey(related_name='kits', verbose_name='Test Manufacturer', blank=True, to='webapp.TestManufacturer', null=True)),
                ('test_model', models.ForeignKey(related_name='kits', verbose_name='Test Model', blank=True, to='webapp.TestModel', null=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Is still in use')),
                ('user', models.ForeignKey(related_name='kits', verbose_name='Owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Test Kit',
                'verbose_name_plural': 'Test Kits',
                'permissions': (('access_to_all_test_kits', "Access to all testers' kits"), ('access_to_pws_test_kits', "Access to own PWS' testers' kits")),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='hazard',
            name='hazard_degree',
            field=models.ForeignKey(related_name='hazards', verbose_name='Hazard Degree', blank=True, to='webapp.HazardDegree', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='test_kit',
            field=models.ForeignKey(related_name='tests', verbose_name='Test Kit', blank=True, to='webapp.TestKit', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='test',
            name='tester_cert',
            field=models.ForeignKey(related_name='tests', verbose_name='Tester Cert', blank=True, to='webapp.TesterCert', null=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='employee',
            name='cert_date',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='cert_expires',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='cert_number',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='test_last_cert',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='test_manufacturer',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='test_model',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='test_serial',
        ),
        migrations.RemoveField(
            model_name='test',
            name='test_last_cert',
        ),
        migrations.RemoveField(
            model_name='test',
            name='test_manufacturer',
        ),
        migrations.RemoveField(
            model_name='test',
            name='test_model',
        ),
        migrations.RemoveField(
            model_name='test',
            name='test_serial',
        )
    ]
