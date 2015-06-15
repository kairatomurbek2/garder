from webapp.models import PWS, LetterType

def add_lettertype_for_existing_pws():
    for pws in PWS.objects.all():
        if not pws.letter_types.exists():
            default_letter_types = LetterType.objects.filter(pws=None)
            for letter_type in default_letter_types:
                letter_type.pk = None
                letter_type.pws = pws
                letter_type.save()
