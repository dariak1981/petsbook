from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('featured_listings', views.index, name='listings'),
    path('<int:listing_id>', views.listing, name='listing'),
    path('searchlistings', views.searchlistings, name='searchlistings'),
]
