from django.shortcuts import render
from listings.choices import price_choices
from listings.models import Listing, Category, Taps, Age, Breeds
from listings.forms import *
from .models import WelcomeText, Services, Terms
from products.models import Product, ProductCategory
from carts.models import Cart
from django.conf import settings
User = settings.AUTH_USER_MODEL
Profile = settings.AUTH_PROFILE_MODULE
from accounts.models import Profile
from django.contrib.auth import get_user_model
User = get_user_model()

def home(request):
  listings = Listing.objects.order_by('-created').filter(adstatus_id = '2')[:4]
  categories = Category.objects.all()
  types = Taps.objects.all()
  ages = Age.objects.all()
  breeds = Breeds.objects.order_by('type_id', 'title_ru')
  services = Services.objects.all()
  welcometext = WelcomeText.objects.first()
  products = Product.objects.order_by('-created').filter(adstatus_id = '2')[:3]
  product_categories = ProductCategory.objects.all()
  cart_obj, new_obj = Cart.objects.new_or_get(request)
  sponsors = Profile.objects.filter(user__is_sponsor=True)

  context = {
    'listings': listings,
    'categories': categories,
    'types': types,
    'ages': ages,
    'price_choices': price_choices,
    'breeds': breeds,
    'services': services,
    'welcometext': welcometext,
    'object_list': products,
    'category_links': product_categories,
    'cart':cart_obj,
    'sponsors': sponsors,
  }

  return render(request, 'pages/home.html', context)

def terms(request):
    terms = Terms.objects.first()

    context = {
      'terms': terms
    }

    return render(request, 'pages/terms.html', context)
