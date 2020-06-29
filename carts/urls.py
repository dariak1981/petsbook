from django.contrib import admin
from django.urls import path
from . import views

app_name = 'carts'

urlpatterns = [
    path('wishlist_update/', views.cart_update, name='update'),
    path('wishlist_update_products/', views.cart_products_update, name='products_update'),
    path('add/<int:product_id>', views.add_cart, name='add_cart'),
    path('details', views.cart_detail, name='cart_detail'),
    path('remove/<int:product_id>', views.cart_remove, name='cart_remove'),
    path('delete_product/<int:product_id>', views.cart_delete_product, name='cart_delete'),
  ]
