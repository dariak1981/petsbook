from django.contrib import admin
from .models import Tag

class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'title', 'title_ru')
    list_editable = ['title', 'title_ru']
    list_display_links = ('id', 'slug')
    search_fields = ('message',)

admin.site.register(Tag, TagAdmin)
