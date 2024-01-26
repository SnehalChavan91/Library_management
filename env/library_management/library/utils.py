import string
import random
from .models import Author

def generate_registration_code(user):
    city_code=user.author.city[:3].upper()
    user_count=Author.objects.filter(city=user.author.city).count()+1
    registration_code = f'AR{city_code}{user_count:04d}'
    return registration_code