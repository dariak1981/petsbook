from django.contrib import admin
from django.urls import path

from . import views
from .views import (
    ProductListView,
    ProductDetailSlugView,
    ProductSearchView,
    ProductCategoryView
)

app_name = 'products'

urlpatterns = [
    path('list/', ProductListView.as_view(), name='products-view'),
    path('category/<slug:category_slug>', ProductCategoryView.as_view(), name='category-view'),
    path('product-search/', ProductSearchView.as_view(), name='product-search'),
    path('<slug:slug>', ProductDetailSlugView.as_view(), name='detail'),
]
