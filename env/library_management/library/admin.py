from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Book)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'city', 'registration_code')
    search_fields = ('name', 'email', 'city', 'registration_code')

#admin.site.register(AuthorAdmin)