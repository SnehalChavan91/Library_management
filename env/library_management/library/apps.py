#from django.apps import AppConfig


#class LibraryConfig(AppConfig):
 #   default_auto_field = "django.db.models.BigAutoField"
  #  name = "library"

from django.apps import AppConfig
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from library_management.library.models import Author
from library_management.library.utils import generate_registration_code


class libraryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "library"

    def ready(self):
        import library_management.library.signals

        post_save.connect(create_author, sender=User)