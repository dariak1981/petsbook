from django.contrib import admin
from .models import ProductCategory, Adstatus, Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', '__str__', 'price', 'city', 'adstatus_id', 'category_id', 'slug']
    list_editable = ['adstatus_id', 'category_id']
    class Meta:
        model = Product

admin.site.register(ProductCategory)
admin.site.register(Adstatus)
admin.site.register(Product, ProductAdmin)
