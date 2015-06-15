# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0018_auto_20150609_0648'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lettertype',
            options={'ordering': ('letter_type',), 'verbose_name': 'Letter Type', 'verbose_name_plural': 'Letter Types', 'permissions': (('browse_lettertype', 'Can browse Letter Type'), ('access_to_all_lettertypes', 'Has access to all Letter Types'), ('access_to_pws_lettertypes', "Has access to PWS's Letter Types"))},
        ),
        migrations.AddField(
            model_name='lettertype',
            name='pws',
            field=models.ForeignKey(default=None, to='webapp.PWS', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='lettertype',
            unique_together=set([('letter_type', 'pws')]),
        ),
    ]
