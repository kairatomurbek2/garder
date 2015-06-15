from django.db.models.signals import post_save
from django.dispatch import receiver
from webapp.models import PWS, LetterType


@receiver(post_save, sender=PWS)
def create_letter_types_for_pws(sender, instance, created, raw, **kwargs):
    if created and not raw:
        default_letter_types = LetterType.objects.filter(pws=None)
        for letter_type in default_letter_types:
            letter_type.pk = None
            letter_type.pws = instance
            letter_type.save()
