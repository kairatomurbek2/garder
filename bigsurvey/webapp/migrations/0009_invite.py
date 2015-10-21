# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webapp', '0008_auto_20151019_0921'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('invite_date', models.DateField(auto_now_add=True, verbose_name='Invite sending date')),
                ('accepted', models.BooleanField(default=False)),
                ('code', models.CharField(default=uuid.uuid4, max_length=64)),
                ('invite_from', models.ForeignKey(related_name='invites_sent', verbose_name='Invite sender', to=settings.AUTH_USER_MODEL)),
                ('invite_pws', models.ManyToManyField(to='webapp.PWS', verbose_name='Invite to PWS')),
                ('invite_to', models.ForeignKey(related_name='invites_received', verbose_name='Invited tester', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Invite',
                'verbose_name_plural': 'Invites',
            },
            bases=(models.Model,),
        ),
    ]
