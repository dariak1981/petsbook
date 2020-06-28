from django.contrib import admin
from .models import Intro, Guidance

class GuidanceAdmin(admin.ModelAdmin):
     list_display = ('id', 'title_ru', 'title')
     list_display_links = ('id', 'title_ru', 'title')
     list_per_page = 25

class IntroAdmin(admin.ModelAdmin):
     list_display = ('id', 'title_ru', 'title')
     list_display_links = ('id', 'title_ru', 'title')


admin.site.register(Intro, IntroAdmin)
admin.site.register(Guidance, GuidanceAdmin)
