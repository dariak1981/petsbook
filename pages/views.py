from django.shortcuts import render
from listings.choices import price_choices
from listings.models import Listing, Category, Taps, Age, Breeds
from listings.forms import *
from .models import WelcomeText, Services, Terms
from products.models import Product, ProductCategory

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
  }

  return render(request, 'pages/home.html', context)

def terms(request):
    terms = Terms.objects.first()

    context = {
      'terms': terms
    }

    return render(request, 'pages/terms.html', context)
