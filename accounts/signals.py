from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserAdditionalInformation

@receiver(post_save, sender=User)
def create_useradditionalinformation(sender, instance, created, **kwargs):
    if created:
        UserAdditionalInformation.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_useradditionalinformation(sender, instance, **kwargs):
    instance.useradditionalinformation.save()

