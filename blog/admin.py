from django.contrib import admin

from .models import Message, Post, Themes

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'message', 'post')
    list_display_links = ('id', 'author')
    search_fields = ('message',)


class ThemesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'title_ru')

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'is_featured', 'title', 'created')
    list_display_links = ('id', 'title')
    list_filter = ('theme', 'author')
    list_per_page = 25


admin.site.register(Message, MessageAdmin)
admin.site.register(Themes, ThemesAdmin)
admin.site.register(Post, PostAdmin)
