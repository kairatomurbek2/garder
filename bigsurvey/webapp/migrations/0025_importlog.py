# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webapp', '0024_auto_20150616_0953'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('added_sites', models.ManyToManyField(related_name='added_imports', to='webapp.Site')),
                ('deactivated_sites', models.ManyToManyField(related_name='deactivated_imports', to='webapp.Site')),
                ('updated_sites', models.ManyToManyField(related_name='updated_imports', to='webapp.Site')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
