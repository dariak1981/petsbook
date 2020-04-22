from django.contrib import admin

from .models import WelcomeText, Services, Terms, FooterText

class WelcomeTextAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'title_ru')
    list_display_links = ('id', 'title')

class ServicesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'title_ru', 'content', 'content_ru')
    list_display_links = ('id', 'title')


class TermsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'title_ru')
    list_display_links = ('id', 'title')

class FooterTextAdmin(admin.ModelAdmin):
    list_display = ('id', 'sitename', 'middletext', 'middletext_ru', 'email')
    list_display_links = ('id', 'sitename')



admin.site.register(WelcomeText, WelcomeTextAdmin)
admin.site.register(Services, ServicesAdmin)
admin.site.register(Terms, TermsAdmin)
admin.site.register(FooterText, FooterTextAdmin)
