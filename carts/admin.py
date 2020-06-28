from django.contrib import admin
from .models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
    list_display_links = ['id', 'user']
    class Meta:
        model = Cart

admin.site.register(Cart, CartAdmin)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'cart']
    list_display_links = ['id', 'product', 'cart']
    class Meta:
        model = Cart

admin.site.register(CartItem, CartItemAdmin)
