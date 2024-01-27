import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Author
from .utils import generate_registration_code
from rest_framework.authtoken.models import Token

logger=logging.getLogger(__name__)
@receiver(post_save,sender=User)

def create_author(sender,instance,created,**kwargs):
    if created:
        registration_code = generate_registration_code(instance)
        Author.objects.create(user=instance,registration_code=registration_code)

        logger.info(f"Registration code {registration_code} created for user{instance.username}")

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)