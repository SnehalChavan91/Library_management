from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from library_management.library.models import Author
from library_management.library.utils import generate_registration_code

@receiver(post_save,sender=User)

def create_author(sender,instance,created,**kwargs):
    if created:
        registration_code = generate_registration_code(instance)
        Author.objects.create(user=instance,registration_code=registration_code)