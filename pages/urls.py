from django.urls import path

from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('terms_and_conditions', views.terms, name='terms'),
]
