from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from datetime import date, datetime
from django.utils.timezone import utc
from django.conf import settings
User = settings.AUTH_USER_MODEL
Profile = settings.AUTH_PROFILE_MODULE
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from django.template import context
from django.urls import reverse
from django.forms import models as forms_models
import csv, io
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils import timezone

from listings.models import Listing, Category, Taps, Gender, Condition, Health, Adstatus, Age, Breeds
from .models import Contact, Contactstype, Contactsgroup
from accounts.models import UserType, Profile
from marketing.forms import MarketingPreferenceForm
from marketing.models import MarketingPreference, marketing_pref_update_receiver
from .forms import ListingForm, ContactForm, ArchiveForm, UserForm, AttachContactsForm, AttachRequestForm, RemoveRequestForm
from blog.models import Post, Message
from analysis.models import ObjectViewed
from . import forms
from django.utils.translation import ugettext as _

User = get_user_model()

@login_required
def profile(request):
     mainuser = get_object_or_404(User, id=request.user.id)
     edituser = get_object_or_404(Profile, user=request.user)
     usertypes = UserType.objects.all()
     activeads = Listing.objects.filter(user_id=request.user.id).filter(adstatus_id = '2').count()
     subscription = MarketingPreference.objects.get(user=request.user)

     context = {
     'mainuser': mainuser,
     'edituser': edituser,
     'usertypes': usertypes,
     'activeads': activeads,
     'subscription': subscription,
     }

     if request.method == "POST" and 'userprofile' in request.POST:
         mainuser.user = request.user
         mainuser.username = request.POST['username']
         mainuser.full_name = request.POST['full_name']
         edituser.usertype = UserType.objects.get(id=request.POST['usertype'])
         edituser.publicmail = request.POST['publicmail']
         edituser.business = request.POST['business']
         edituser.phone = request.POST['phone']
         edituser.links = request.POST['links']
         edituser.description = request.POST['description']
         if 'image-clear' in request.POST:
             edituser.photo = None
         else:
             if request.FILES.get('photo'):
                 edituser.photo = request.FILES.get('photo')
             else:
                 edituser.photo = edituser.photo
         edituser.ad_organization = request.POST['ad_organization']
         edituser.ad_address = request.POST['ad_address']
         edituser.ad_website = request.POST['ad_website']
         edituser.ad_email = request.POST['ad_email']
         edituser.ad_youtube = request.POST['ad_youtube']
         edituser.ad_facebook = request.POST['ad_facebook']
         edituser.ad_vk = request.POST['ad_vk']

         mainuser.save()
         edituser.save()
         return redirect('profile')

     if request.method=="POST" and 'marketing' in request.POST:
         if request.user.is_authenticated:
             if subscription.subscribed == True:
                 subscription.subscribed = False
                 subscription.save()
             else:
                 subscription.subscribed = True
                 subscription.save()
         else:
             return redirect('login')

     return render(request, 'user/profile.html', context)


@login_required
def dashboard(request):
  publishedlistings = Listing.objects.order_by('-created').filter(user_id=request.user.id).filter(adstatus_id = '2')[:3]
  activelistings = Listing.objects.filter(user_id=request.user.id).filter(adstatus_id = '2').count()
  hiddenlistings = Listing.objects.filter(user_id=request.user.id).filter(adstatus_id = '1').count()
  archivedlistings = Listing.objects.filter(user_id=request.user.id).filter(adstatus_id = '3').count()
  userposts = Post.objects.filter(author=request.user.id).count()
  usermessages = Message.objects.filter(author=request.user.id).count()
  sitecontacts = Contact.objects.filter(user=request.user.id).count()
  pendingtime = Listing.objects.order_by('-created').filter(user_id=request.user.id).filter(adstatus_id = '2')[:1]
  views = request.user.objectviewed_set.by_model(Listing)[:18]
  # viewed_ids = []
  # for x in viewed_ids:
  #     viewed_ids.append(x.object_id)
  # viewed_ids = [x.object_id for x in objects_viewed]
  # views = Listing.objects.filter(pk__in=viewed_ids)

  context = {
     'publishedlistings': publishedlistings,
     'activelistings': activelistings,
     'hiddenlistings': hiddenlistings,
     'archivedlistings': archivedlistings,
     'userposts': userposts,
     'usermessages': usermessages,
     'sitecontacts': sitecontacts,
     'pendingtime': pendingtime,
     'views': views,
    }

  return render(request, 'user/index.html', context)

@login_required
def posts(request, id=None):
    listings = Listing.objects.all().filter(user_id=request.user.id).order_by('-archived')
    contacts = Contact.objects.filter(user_id=request.user.id)

    if 'delete' in request.POST and 'instance' in request.POST:
        id_selected = request.POST.get('instance')
        listing = Listing.objects.get(id=id_selected)
        listing.delete()

    if 'bystatus' in request.POST:
        listings = listings.order_by('adstatus_id')

    if 'bydate' in request.POST:
        listings = listings.order_by('-created')


    if 'publish' in request.POST and 'instance' in request.POST:
        i = request.POST.get('instance')
        listing = Listing.objects.get(id=i)
        listing.adstatus_id_id = '2'
        listing.created = timezone.now()
        listing.owner = None
        listing.save()
        return redirect('dashboard')

    if 'editrecord' in request.POST and 'instance' in request.POST:
        i = request.POST.get('instance')
        listing = Listing.objects.get(id=i)
        return redirect('editlisting', listing_id=listing.id)

    if 'sendtoarchive' in request.POST and 'instance' in request.POST:
        i = request.POST.get('instance')
        listing = Listing.objects.get(id=i)
        listing.adstatus_id_id = '3'
        listing.save()
        return redirect('posts')

    if 'restore' in request.POST and 'instance' in request.POST:
        i = request.POST.get('instance')
        listing = Listing.objects.get(id=i)
        listing.adstatus_id_id = '1'
        listing.save()
        return redirect('posts')

    if 'addrequest' in request.POST and 'instance' in request.POST:
        i = request.POST.get('instance')
        listing = Listing.objects.get(id=i)
        return redirect('requested', listing_id=listing.id)

    if 'editowner' in request.POST and 'instance' in request.POST:
        i = request.POST.get('instance')
        listing = Listing.objects.get(id=i)
        return redirect('archived', listing_id=listing.id)

    if 'attachfosterer' in request.POST and 'instance' in request.POST:
        i = request.POST.get('instance')
        listing = Listing.objects.get(id=i)
        return redirect('forested', listing_id=listing.id)

    if 'export' in request.POST:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Listings.csv"'
        response.write(u'\ufeff'.encode('utf8'))

        writer = csv.writer(response, delimiter=',')
        writer.writerow(['Title', 'Category', 'Price', 'Type', 'Breed', 'Age', 'Health', 'Description'])

        for listing in Listing.objects.all().filter(user_id=request.user.id).values_list('title', 'category_id__title', 'price', 'types_id__title', 'breeds__title', 'age_id__title', 'health_id__title', 'description'):
            writer.writerow(listing)

        return response

    if 'export_ru' in request.POST:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Export.csv"'
        response.write(u'\ufeff'.encode('utf8'))

        writer = csv.writer(response, delimiter=',')
        writer.writerow(['Заголовок', 'Категория', 'Цена', 'Раздел', 'Порода', 'Возраст', 'Здоровье', 'Описание'])

        for listing in Listing.objects.all().filter(user_id=request.user.id).values_list('title', 'category_id__title_ru', 'price', 'types_id__title_ru', 'breeds__title_ru', 'age_id__title_ru', 'health_id__title_ru', 'description'):
            writer.writerow(listing)

        return response

    paginator = Paginator(listings, 5)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings,
        'contacts': contacts,
    }

    return render(request, 'user/posts.html', context)

@login_required
def newlisting(request):
    healths = Health.objects.all()
    categories = Category.objects.all()
    breeds = Breeds.objects.order_by('type_id', 'title_ru')
    ages = Age.objects.all()
    genders = Gender.objects.all()
    conditions = Condition.objects.all()
    types = Taps.objects.all()
    if request.method == "POST":
        user = request.user
        user_contact = request.POST['user_contact']
        title = request.POST['title']
        category = Category.objects.get(id=request.POST['category'])
        type = Taps.objects.get(id=request.POST['type'])
        city = request.POST['city']
        district = request.POST['district']
        price = request.POST['price']
        breed = Breeds.objects.get(id=request.POST['breed'])
        age = Age.objects.get(id=request.POST['age'])
        gender = Gender.objects.get(id=request.POST['gender'])
        condition = Condition.objects.get(id=request.POST['condition'])
        health = Health.objects.get(id=request.POST['health'])
        video = request.POST['video']
        description = request.POST['description']
        photo_main = request.FILES.get('photo_main')
        photo_1 = request.FILES.get('photo_1')
        photo_2 = request.FILES.get('photo_2')
        photo_3 = request.FILES.get('photo_3')
        photo_4 = request.FILES.get('photo_4')

        newlisting = Listing(
        user=user, user_contact=user_contact, title=title, category_id=category, types_id=type, city=city, district=district,
        price=price, breeds=breed, age_id=age, gender_id=gender, conditions_id=condition, health_id=health, video=video,
        description=description, photo_main=photo_main, photo_1=photo_1, photo_2=photo_2, photo_3=photo_3, photo_4=photo_4)

        newlisting.save()

        messages.success(request, 'New listing is registered')
        return redirect('posts')

    context = {
    'healths': healths,
    'categories': categories,
    'breeds': breeds,
    'ages': ages,
    'genders': genders,
    'conditions':conditions,
    'types': types,
    }

    return render(request, 'user/newlisting.html', context)


@login_required
def editlisting(request, listing_id):
  editlisting = Listing.objects.get(pk=listing_id)
  healths = Health.objects.all()
  categories = Category.objects.all()
  breeds = Breeds.objects.order_by('type_id', 'title_ru')
  ages = Age.objects.all()
  genders = Gender.objects.all()
  conditions = Condition.objects.all()
  types = Taps.objects.all()
  contacts = Contact.objects.filter(user_id=request.user.id)

  context = {
  'editlisting': editlisting,
  'healths': healths,
  'categories': categories,
  'breeds': breeds,
  'ages': ages,
  'genders': genders,
  'conditions':conditions,
  'types': types,
  'contacts': contacts,
  }

  if request.method == "POST":
      editlisting.user = request.user
      editlisting.user_contact = request.POST['user_contact']
      editlisting.title = request.POST['title']
      editlisting.category_id = Category.objects.get(id=request.POST['category'])
      editlisting.types_id = Taps.objects.get(id=request.POST['type'])
      editlisting.city = request.POST['city']
      editlisting.district = request.POST['district']
      editlisting.price = request.POST['price']
      editlisting.breeds = Breeds.objects.get(id=request.POST['breed'])
      editlisting.age_id = Age.objects.get(id=request.POST['age'])
      editlisting.gender_id = Gender.objects.get(id=request.POST['gender'])
      editlisting.conditions_id = Condition.objects.get(id=request.POST['condition'])
      editlisting.health_id = Health.objects.get(id=request.POST['health'])

      if 'owner' in request.POST:
          if request.POST['owner'] == '':
              editlisting.owner = None
          else:
              editlisting.owner = Contact.objects.get(id=request.POST['owner'])
      else:
          editlisting.owner = editlisting.owner

      if 'forester' in request.POST:
          if request.POST['forester'] == '':
              editlisting.forester = None
          else:
              editlisting.forester = Contact.objects.get(id=request.POST['forester'])
      else:
          editlisting.forester = editlisting.forester

      editlisting.video = request.POST['video']
      editlisting.description = request.POST['description']

      if 'image-clear' in request.POST:
          editlisting.photo_main = None
      else:
          if request.FILES.get('photo_main'):
              editlisting.photo_main = request.FILES.get('photo_main')
          else:
              editlisting.photo_main = editlisting.photo_main
      if 'image-clear1' in request.POST:
          editlisting.photo_1 = None
      else:
          if request.FILES.get('photo_1'):
              editlisting.photo_1 = request.FILES.get('photo_1')
          else:
              editlisting.photo_1 = editlisting.photo_1
      if 'image-clear2' in request.POST:
          editlisting.photo_2 = None
      else:
          if request.FILES.get('photo_2'):
              editlisting.photo_2 = request.FILES.get('photo_2')
          else:
              editlisting.photo_2 = editlisting.photo_2
      if 'image-clear3' in request.POST:
          editlisting.photo_3 = None
      else:
          if request.FILES.get('photo_3'):
              editlisting.photo_3 = request.FILES.get('photo_3')
          else:
              editlisting.photo_3 = editlisting.photo_3
      if 'image-clear4' in request.POST:
          editlisting.photo_4 = None
      else:
          if request.FILES.get('photo_4'):
              editlisting.photo_4 = request.FILES.get('photo_4')
          else:
              editlisting.photo_4 = editlisting.photo_4


      editlisting.save()
      return redirect('posts')

  return render(request, 'user/editlisting.html', context)



@login_required
def archived(request, listing_id):
    archived = get_object_or_404(Listing, pk=listing_id)
    form = ArchiveForm(request.POST or None, instance=archived)
    form.fields['owner'].queryset = Contact.objects.all().filter(user_id=request.user.id)

    context = {
        'archived': archived,
        "form": form,
    }


    if request.method == "POST":
      form = ArchiveForm(request.POST, instance=archived)
      if form.is_valid():
          form = form.save(commit=False)
          form.adstatus_id = get_object_or_404(Adstatus, pk=3)
          form.save()
          return redirect('posts')
      else:
          form = ArchiveForm(instance=archived)

    return render(request, 'user/archived.html', context)

@login_required
def forested(request, listing_id):
    forested = get_object_or_404(Listing, pk=listing_id)
    form = AttachContactsForm(request.POST or None, instance=forested)
    form.fields['forester'].queryset = Contact.objects.all().filter(user_id=request.user.id)

    context = {
        'forested': forested,
        "form": form,
    }


    if request.method == "POST":
      form = AttachContactsForm(request.POST, instance=forested)
      if form.is_valid():
          form = form.save(commit=False)
          form.adstatus_id = get_object_or_404(Adstatus, pk=4)
          form.save()
          return redirect('posts')
      else:
          form = AttachContactsForm(instance=forested)

    return render(request, 'user/forested.html', context)

@login_required
def requested(request, listing_id):
    requested = get_object_or_404(Listing, pk=listing_id)
    attachedrequests = Contact.objects.filter(attached_id=listing_id).filter(user_id=request.user.id)
    contacts = Contact.objects.filter(user_id=request.user.id).exclude(attached_id=listing_id)
    form = RemoveRequestForm(request.POST)

    context = {
        'requested': requested,
        'attachedrequests':attachedrequests,
        'contacts':contacts,
        "form": form,
    }

    if request.method=="POST" and 'addrequest' in request.POST:
        id_selected = request.POST.get('contact')
        if id_selected != '':
            contact = Contact.objects.get(id=id_selected)
            contact.attached_id = listing_id
            contact.save()
            return redirect('posts')
        else:
            return redirect('posts')

    if request.method=="POST" and 'removerequest' in request.POST:
        form = RemoveRequestForm(request.POST or None)
        if form.is_valid():
            is_checked = request.POST.getlist('checkedid')

            for i in is_checked:
                contact = Contact.objects.get(id=i)
                form = RemoveRequestForm(request.POST, instance = contact)
                form.attached_id = None
                form.save()
            return redirect('posts')
        else:
            form = RemoveRequestForm()

    return render(request, 'user/requested.html', context)


@login_required
def contacts(request):
    contacts = Contact.objects.filter(user_id=request.user.id).order_by('-created')

    if 'editcontact' in request.POST and 'instance' in request.POST:
        i = request.POST.get('instance')
        editcont = Contact.objects.get(id=i)
        return redirect('editcontact', contact_id=editcont.id)

    if 'delete' in request.POST and 'instance' in request.POST:
        i = request.POST.get('instance')
        contacts = Contact.objects.filter(id=i)
        contacts.delete()
        return redirect('contacts')

    if 'bygroup' in request.POST:
        contacts = contacts.order_by('group')

    if 'bytype' in request.POST:
        contacts = contacts.order_by('type')

    if 'export' in request.POST:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Contacts.csv"'
        response.write(u'\ufeff'.encode('utf8'))

        writer = csv.writer(response, delimiter=',')
        writer.writerow(['Name', 'Type', 'Group', 'Phone', 'Address', 'Links', 'Comments', 'Created'])

        for contact in Contact.objects.all().filter(user_id=request.user.id).values_list('name', 'type__title', 'group', 'phone', 'address', 'links', 'comments', 'created'):
            writer.writerow(contact)

        return response

    if 'export_ru' in request.POST:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Export_Contacts.csv"'
        response.write(u'\ufeff'.encode('utf8'))

        writer = csv.writer(response, delimiter=',')
        writer.writerow(['Имя', 'Тип владельца', 'Группа', 'Телефон', 'Адрес', 'Ссылки', 'Комментарии', 'Дата создания'])

        for contact in Contact.objects.all().filter(user_id=request.user.id).values_list('name', 'type__title_ru', 'group', 'phone', 'address', 'links', 'comments', 'created'):
            writer.writerow(contact)

        return response


    paginator = Paginator(contacts, 5)
    page = request.GET.get('page')
    paged_contacts = paginator.get_page(page)


    context = {
     'contacts': paged_contacts
     }


    return render(request, 'user/responsible.html', context)


@login_required
def newcontact(request):
    types = Contactstype.objects.all()
    groups = Contactsgroup.objects.all()
    listings = Listing.objects.filter(user_id=request.user.id)
    if request.method == "POST":
        user = request.user
        type = Contactstype.objects.get(id=request.POST['type'])
        group = Contactsgroup.objects.get(id=request.POST['group'])
        name = request.POST['name']
        address = request.POST['address']
        phone = request.POST['phone']
        links = request.POST['links']
        if 'listings' in request.POST:
            if request.POST['listings'] == '':
                attached = None
            else:
                attached = Listing.objects.get(id=request.POST['listings'])
        else:
            attached = None
        comments = request.POST['comments']

        newcontact = Contact(
        user=user, type=type, group=group, name=name, address=address, phone=phone, links=links, attached=attached, comments=comments
        )

        newcontact.save()

        return redirect('contacts')

    context = {
    'types': types,
    'groups': groups,
    'listings': listings
    }

    return render(request, 'user/newcontact.html', context)

@login_required
def editcontact(request, contact_id):
    editcontact = Contact.objects.get(pk=contact_id)
    types = Contactstype.objects.all()
    groups = Contactsgroup.objects.all()

    context = {
    'types': types,
    'groups': groups,
    'editcontact': editcontact,
    }

    if request.method == "POST" and 'type' in request.POST:
        editcontact.user = request.user
        editcontact.type = Contactstype.objects.get(id=request.POST['type'])
        editcontact.group = Contactsgroup.objects.get(id=request.POST['group'])
        editcontact.name = request.POST['name']
        editcontact.address = request.POST['address']
        editcontact.phone = request.POST['phone']
        editcontact.links = request.POST['links']
        if 'listings' in request.POST:
            if request.POST['listings'] == '':
                editcontact.attached = None
            else:
                editcontact.attached = Listing.objects.get(id=request.POST['listings'])
        else:
            editcontact.attached = editcontact.attached
        editcontact.comments = request.POST['comments']

        editcontact.save()
        return redirect('contacts')



    return render(request, 'user/editcontact.html', context)
