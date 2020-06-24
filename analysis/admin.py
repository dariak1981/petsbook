from django.contrib import admin

from .models import ObjectViewed, UserSession

class UserSessionAdmin(admin.ModelAdmin):
     list_display = ('id', 'user', 'ip_address', 'timestamp', 'active', 'ended')
     list_display_links = ('id', 'user', 'ip_address')
     list_per_page = 25

class ObjectViewedAdmin(admin.ModelAdmin):
     list_display = ('id', 'user', 'ip_address', 'content_type', 'timestamp')
     list_display_links = ('id', 'user', 'ip_address')
     list_per_page = 25


admin.site.register(ObjectViewed, ObjectViewedAdmin)
admin.site.register(UserSession, UserSessionAdmin)
