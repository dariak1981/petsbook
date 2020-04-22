from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Contact, Contactstype, Contactsgroup, UserType

class UserProfileInline(admin.StackedInline):

    model = UserProfile
    # list_display = ('phone', 'usergroup', 'business')
    max_num = 1
    verbose_name_plural = ('profile')

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )


class ContactstypeAdmin(admin.ModelAdmin):
     list_display = ('id', 'title', 'title_ru')
     list_per_page = 25

class UserTypeAdmin(admin.ModelAdmin):
     list_display = ('id', 'title', 'title_ru')
     list_per_page = 25

# # Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserType, UserTypeAdmin)
admin.site.register(Contact)
admin.site.register(Contactstype, ContactstypeAdmin)
admin.site.register(Contactsgroup)
