from .models import Account, VerificationCode
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Account)
def post_save_generate_code(sender, instance, created, *args, **kwargs):
    if created:
        VerificationCode.objects.create(user = instance)