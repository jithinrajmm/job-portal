from accounts.models import Account

from django.dispatch import receiver

from django.db.models.signals import post_save


@receiver(post_save,sender=Account)
def profile_create_from_user(sender,instance,created,*args,**kwargs):
    if created:
        instance.is_active = True
        instance.save()
