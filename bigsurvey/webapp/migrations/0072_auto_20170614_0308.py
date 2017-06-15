# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from django.db import models, migrations

PLACEHOLDERS = [("{CustomerZip}", '{MailingZip}'), ('{CustomerCity}', '{MailingCity}'),
                ('{CustomerState}', '{MailingState}'), ('{CustomerAddress}', '{MailingAddress}')]


def change_data_placeholder_letter_type(apps, chema_editor):
    LetterType = apps.get_model('webapp', 'LetterType')
    for item in LetterType.objects.all():
        for old_t, new_t in PLACEHOLDERS:
            item.template = re.sub(old_t, new_t, item.template)
        item.save()


class Migration(migrations.Migration):
    dependencies = [
        ('webapp', '0071_auto_20170613_0231'),
    ]

    operations = [
        migrations.RunPython(change_data_placeholder_letter_type)
    ]
