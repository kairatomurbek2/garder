# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def add_letter_types_for_existing_pws(apps, schema_editor):
    PWS = apps.get_model("webapp", "PWS")
    LetterType = apps.get_model("webapp", "LetterType")
    default_letter_types = LetterType.objects.filter(pws=None)
    for pws in PWS.objects.all():
        for letter_type in default_letter_types:
            if not pws.letter_types.filter(letter_type=letter_type.letter_type).exists():
                letter_type.pk = None
                pws.letter_types.add(letter_type)


class Migration(migrations.Migration):
    dependencies = [
        ('webapp', '0027_auto_20150622_0928'),
    ]

    operations = [
        migrations.RunPython(add_letter_types_for_existing_pws),
    ]
