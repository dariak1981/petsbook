from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('info', views.contact, name='support'),
    path('guidance', views.guidance, name='guidance'),
]
