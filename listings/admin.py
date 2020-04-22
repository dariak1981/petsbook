from django.contrib import admin

from .models import Listing, Category, Taps, Breeds, Gender, Condition, Health, Adstatus, Age

class ListingAdmin(admin.ModelAdmin):
     list_display = ('id', 'title', 'user', 'owner', 'created', 'adstatus_id', 'types_id', 'category_id','is_featured', 'city', 'price')
     list_display_links = ('id', 'title')
     list_filter = ('category_id', 'user',)
     search_fields = ('title_id', 'description', 'city', 'district', 'price')
     list_per_page = 25


class AgeAdmin(admin.ModelAdmin):
     list_display = ('id', 'title', 'title_ru')
     list_per_page = 25

class GenderAdmin(admin.ModelAdmin):
     list_display = ('id', 'title', 'title_ru')
     list_per_page = 25

class ConditionAdmin(admin.ModelAdmin):
     list_display = ('id', 'title', 'title_ru')
     list_per_page = 25

class HealthAdmin(admin.ModelAdmin):
     list_display = ('id', 'title', 'title_ru')
     list_per_page = 25

class CategoryAdmin(admin.ModelAdmin):
     list_display = ('id', 'title', 'title_ru')
     list_per_page = 25

class AdstatusAdmin(admin.ModelAdmin):
     list_display = ('id', 'title')
     list_per_page = 25

class TapsAdmin(admin.ModelAdmin):
     list_display = ('id', 'title', 'title_ru')
     list_per_page = 25

class BreedsAdmin(admin.ModelAdmin):
     list_display = ('id', 'type_id', 'title', 'title_ru')
     list_per_page = 25



admin.site.register(Listing, ListingAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Taps, TapsAdmin)
admin.site.register(Gender, GenderAdmin)
admin.site.register(Age, AgeAdmin)
admin.site.register(Condition, ConditionAdmin)
admin.site.register(Health, HealthAdmin)
admin.site.register(Adstatus, AdstatusAdmin)
admin.site.register(Breeds, BreedsAdmin)
