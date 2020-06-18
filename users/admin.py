from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Contact, Contactstype, Contactsgroup


class ContactstypeAdmin(admin.ModelAdmin):
     list_display = ('id', 'title', 'title_ru')
     list_per_page = 25

admin.site.register(Contact)
admin.site.register(Contactstype, ContactstypeAdmin)
admin.site.register(Contactsgroup)
