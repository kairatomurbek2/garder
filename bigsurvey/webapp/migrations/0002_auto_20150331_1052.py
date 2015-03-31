# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('model', models.CharField(max_length=20, verbose_name='Test Model')),
            ],
            options={
                'verbose_name': 'Test Model',
                'verbose_name_plural': 'Test Models',
                'permissions': (('browse_testmodel', 'Can browse Test Models'),),
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='testpermission',
            name='given_by',
        ),
        migrations.RemoveField(
            model_name='testpermission',
            name='given_to',
        ),
        migrations.RemoveField(
            model_name='testpermission',
            name='site',
        ),
        migrations.DeleteModel(
            name='TestPermission',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='certificate',
        ),
        migrations.RemoveField(
            model_name='hazard',
            name='survey',
        ),
        migrations.RemoveField(
            model_name='letter',
            name='hazard',
        ),
        migrations.RemoveField(
            model_name='test',
            name='last_calibration_date',
        ),
        migrations.RemoveField(
            model_name='test',
            name='test_manufacturer',
        ),
        migrations.RemoveField(
            model_name='test',
            name='test_serial_number',
        ),
        migrations.AddField(
            model_name='employee',
            name='cert_date',
            field=models.DateField(null=True, verbose_name='Cert. Date', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employee',
            name='cert_expires',
            field=models.DateField(null=True, verbose_name='Cert. Expires', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employee',
            name='cert_number',
            field=models.CharField(max_length=30, null=True, verbose_name='Cert. Number', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employee',
            name='test_last_cert',
            field=models.DateField(null=True, verbose_name='Last Cert.', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employee',
            name='test_manufacturer',
            field=models.ForeignKey(related_name='testers', verbose_name='Test Manufacturer', blank=True, to='webapp.TestManufacturer', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employee',
            name='test_model',
            field=models.ForeignKey(related_name='testers', verbose_name='Test Model', blank=True, to='webapp.TestModel', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hazard',
            name='is_present',
            field=models.BooleanField(default=True, verbose_name='Is Present On Site'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hazard',
            name='site',
            field=models.ForeignKey(related_name='hazards', default=1, verbose_name='Site', to='webapp.Site'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='survey',
            name='hazards',
            field=models.ManyToManyField(related_name='surveys', null=True, verbose_name='Hazards', to='webapp.Hazard', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='employee',
            name='pws',
            field=models.ForeignKey(related_name='employees', verbose_name='PWS', blank=True, to='webapp.PWS', null=True),
            preserve_default=True,
        ),
    ]
