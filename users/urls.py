from django.urls import path

from . import views

urlpatterns = [
  path('newlisting', views.newlisting, name='newlisting'),
  path('dashboard', views.dashboard, name='dashboard'),
  path('profile', views.profile, name='profile'),
  path('user_ads', views.posts, name='posts'),
  path('user_ads/<int:listing_id>', views.editlisting, name='editlisting'),
  path('archived/<int:listing_id>', views.archived, name='archived'),
  path('fostered/<int:listing_id>', views.forested, name='forested'),
  path('requested/<int:listing_id>', views.requested, name='requested'),
  path('contacts', views.contacts, name='contacts'),
  path('newcontact', views.newcontact, name='newcontact'),
  path('editcontact/<int:contact_id>', views.editcontact, name='editcontact'),
]
