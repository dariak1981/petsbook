from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from datetime import date
from .models import Listing, Category, Taps, Age, Breeds
from blog.models import Post
from .choices import price_choices
from django.contrib.auth.models import User
from pages.models import Services
from users.models import UserProfile

def index(request):
  listings = Listing.objects.order_by('-created').filter(adstatus_id = '2').exclude(category_id = '3')

  paginator = Paginator(listings, 12)
  page = request.GET.get('page')
  paged_listings = paginator.get_page(page)

  context = {
    'listings': paged_listings
   }
  return render(request, 'listings/listings.html', context)

def listing(request, listing_id):
  listing = get_object_or_404(Listing, pk=listing_id)
  services = Services.objects.all()
  field_name = 'user'
  field_value = getattr(listing, field_name)
  activeads = Listing.objects.filter(user_id=field_value).filter(adstatus_id = '2').count()
  featuredlistings = Listing.objects.filter(adstatus_id = '2').exclude(category_id = '3').order_by('-created')[:3]
  field_video = 'video'
  field_video_value = getattr(listing, field_video)
  youtube = field_video_value.rsplit('=', 1)[-1]


  context = {
  'listing':listing,
  'services': services,
  'activeads':activeads,
  'featuredlistings':featuredlistings,
  'youtube':youtube
  }
  return render(request, 'listings/listing.html', context)


def searchlistings(request):
    categories = Category.objects.all()
    types = Taps.objects.all()
    breeds = Breeds.objects.order_by('type_id', 'title_ru')
    ages = Age.objects.all()
    services = Services.objects.all()
    queryset_list = Listing.objects.order_by('-created').filter(adstatus_id = '2')




    # keywords
    if 'keywords' in request.GET:
        keywords = request.GET.get('keywords') or None
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)

    # City
    if 'city' in request.GET:
       city = request.GET.get('city') or None
       if city:
           queryset_list = queryset_list.filter(city__iexact=city)

    # Category
    if 'category' in request.GET:
       category = request.GET.get('category') or None
       if category:
          queryset_list = queryset_list.filter(category_id=category)

    # Type
    if 'type' in request.GET:
       type = request.GET.get('type') or None
       if type:
           queryset_list = queryset_list.filter(types_id=type)

    # Breed
    if 'breed' in request.GET:
       breed = request.GET.get('breed') or None
       if breed:
          queryset_list = queryset_list.filter(breeds=breed)

    # Age
    if 'age' in request.GET:
       age = request.GET.get('age') or None
       if age:
          queryset_list = queryset_list.filter(age_id=age)

    # Price
    if 'price' in request.GET:
       price = request.GET.get('price') or None
       if price:
          queryset_list = queryset_list.filter(price__lte=price)

    paginator = Paginator(queryset_list, 12)
    page = request.GET.get('page')
    paged_queryset_list = paginator.get_page(page)

    context = {
     'listings': paged_queryset_list,
     'categories': categories,
     'types': types,
     'breeds': breeds,
     'ages': ages,
     'price_choices': price_choices,
     'values':request.GET,
     'services': services
    }
    return render(request, 'listings/search.html', context)
