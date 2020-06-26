from django.urls import path

from . import views

urlpatterns = [
  path('dashboard', views.dashboard, name='dashboard'),
  path('profile', views.profile, name='profile'),
  path('user-ads', views.posts, name='posts'),
  path('new-listing', views.newlisting, name='newlisting'),
  path('user-ads/<int:listing_id>', views.editlisting, name='editlisting'),
  path('archived/<int:listing_id>', views.archived, name='archived'),
  path('fostered/<int:listing_id>', views.forested, name='forested'),
  path('requested/<int:listing_id>', views.requested, name='requested'),
  path('contacts', views.contacts, name='contacts'),
  path('new-contact', views.newcontact, name='newcontact'),
  path('edit-contact/<int:contact_id>', views.editcontact, name='editcontact'),
  path('my-proposals', views.product_ads, name='product_ads'),
  path('new-product', views.new_product, name='new_product'),
  path('edit-product/<int:product_id>', views.edit_product, name='edit_product'),
]
