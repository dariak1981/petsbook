from django.contrib import admin

from .models import Propstatus, Proposal, Application

class ProposalAdmin(admin.ModelAdmin):
     list_display = ('id', 'title', 'user', 'city', 'created', 'adstatus_id', 'amount')
     list_display_links = ('id', 'title')
     list_filter = ('city', 'user',)
     search_fields = ('city', 'user')
     list_per_page = 25

class PropstatusAdmin(admin.ModelAdmin):
     list_display = ('id', 'title')

class ApplicationAdmin(admin.ModelAdmin):
     list_display = ('id', 'user', 'created')
     list_display_links = ('id', 'user')

admin.site.register(Proposal, ProposalAdmin)
admin.site.register(Propstatus, PropstatusAdmin)
admin.site.register(Application, ApplicationAdmin)
