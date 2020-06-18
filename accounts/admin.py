from django.contrib import admin
from django.contrib.auth import get_user_model
from .forms import RegisterForm, UserAdminChangeForm
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile, UserType, EmailActivation
User = get_user_model()

class ProfileInline(admin.StackedInline):

    model = Profile
    # list_display = ('phone', 'usergroup', 'business')
    max_num = 1
    verbose_name_plural = ('profile')

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = RegisterForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'email', 'username', 'full_name', 'admin', 'is_active')
    list_filter = ('admin', 'staff', 'is_active',)
    list_display_links = ('id', 'email', 'full_name',)
    readonly_fields=('joined',)
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Personal info', {'fields': ('username', 'full_name', 'joined',)}),
        ('Permissions', {'fields': ('admin', 'staff', 'is_active',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2')}
        ),
    )
    search_fields = ('email', 'username', 'full_name',)
    ordering = ('email',)
    filter_horizontal = ()

class EmailActivationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'email', 'activated', 'forced_expired')
    list_display_links = ('id', 'user', 'email',)
    search_fields = ['email']
    class Meta:
        model = EmailActivation

admin.site.register(EmailActivation, EmailActivationAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(UserType)
admin.site.unregister(Group)
