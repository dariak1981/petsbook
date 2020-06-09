from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from datetime import date, datetime
from django.utils.timezone import utc
from django.contrib.auth.models import User
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
from .models import UserProfile, Contact, Contactstype, Contactsgroup, UserType
from .forms import ListingForm, ContactForm, ArchiveForm, UserForm, UserMainForm, UserRegisterForm, ForesterForm
from blog.models import Post, Message
from . import forms
from django.utils.translation import ugettext as _

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form':form})

@login_required
def profile(request):
     mainuser = get_object_or_404(User, id=request.user.id)
     edituser = get_object_or_404(UserProfile, user=request.user)
     usertypes = UserType.objects.all()

     context = {
     'mainuser': mainuser,
     'edituser': edituser,
     'usertypes': usertypes,
     }

     if request.method == "POST":
         mainuser.user = request.user
         mainuser.email = request.POST['email']
         mainuser.first_name = request.POST['first_name']
         mainuser.last_name = request.POST['last_name']
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


         mainuser.save()
         edituser.save()
         return redirect('profile')

     return render(request, 'users/profile.html', context)

     # //////////////////////////////////////////////////////////////////////
    # mainuser = get_object_or_404(User, id=request.user.id)
    # edituser = get_object_or_404(UserProfile, user=request.user)
    #
    # form1 = UserMainForm(instance=mainuser)
    # form2 = UserForm(instance=edituser)
    #
    # context = {
    #     "edituser": edituser,
    #     "form1":form1,
    #     "form2":form2,
    # }
    #
    # if request.method == 'POST':
    #     form1 = UserMainForm(request.POST, instance=mainuser)
    #     form2 = UserForm(request.POST, request.FILES, instance=edituser)
    #     if form1.is_valid() and form2.is_valid():
    #         form1.save()
    #         form2.save()
    #         return redirect('profile')
    # else:
    #     form1 = UserMainForm(instance=mainuser)
    #     form2 = UserForm(instance=edituser)
    #
    #
    # return render(request, 'users/profile.html', context)


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
  datejoined = User.objects.filter(id=request.user.id)
  alllistings = Listing.objects.filter(user_id=request.user.id).count()

  context = {
     'publishedlistings': publishedlistings,
     'activelistings': activelistings,
     'hiddenlistings': hiddenlistings,
     'archivedlistings': archivedlistings,
     'userposts': userposts,
     'usermessages': usermessages,
     'sitecontacts': sitecontacts,
     'pendingtime': pendingtime,
     'datejoined': datejoined,
     'alllistings': alllistings,
    }

  return render(request, 'users/index.html', context)

@login_required
def posts(request, id=None):
    listings = Listing.objects.all().filter(user_id=request.user.id).order_by('-archived')
    contacts = Contact.objects.filter(user_id=request.user.id)

    if 'delete' in request.POST:
        id_list = request.POST.getlist('instance')
        if id_list:
            for i in id_list:
                listings = Listing.objects.filter(id=i)
                for object in listings:
                    object.delete()
                    return redirect('posts')
        else:
            return redirect('posts')

    if 'bystatus' in request.POST:
        listings = listings.order_by('adstatus_id')

    if 'bydate' in request.POST:
        listings = listings.order_by('-created')


    if 'publish' in request.POST:
        id_list = request.POST.getlist('instance')
        if id_list:
            for i in id_list:
                listings = Listing.objects.filter(id=i)
                for object in listings:
                    object.adstatus_id_id = '2'
                    object.created = timezone.now()
                    object.owner = None
                    object.save()
                    return redirect('dashboard')
        else:
            return redirect('posts')


    if 'hide' in request.POST:
        id_list = request.POST.getlist('instance')
        if id_list:
            for i in id_list:
                listings = Listing.objects.filter(id=i)
                for object in listings:
                    object.adstatus_id_id = '1'
                    object.owner = None
                    object.save()
                    return redirect('posts')
        else:
            return redirect('posts')

    if 'restore' in request.POST:
        id_list = request.POST.getlist('instance')
        if id_list:
            for i in id_list:
                listings = Listing.objects.filter(id=i)
                for object in listings:
                    object.adstatus_id_id = '1'
                    object.owner = None
                    object.save()
                    return redirect('posts')

        else:
            return redirect('posts')

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

    return render(request, 'users/posts.html', context)

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
        description = request.POST['description']
        photo_main = request.FILES.get('photo_main')
        photo_1 = request.FILES.get('photo_1')
        photo_2 = request.FILES.get('photo_2')
        photo_3 = request.FILES.get('photo_3')
        photo_4 = request.FILES.get('photo_4')

        newlisting = Listing(
        user=user, user_contact=user_contact, title=title, category_id=category, types_id=type, city=city, district=district,
        price=price, breeds=breed, age_id=age, gender_id=gender, conditions_id=condition, health_id=health,
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

    return render(request, 'users/newlisting.html', context)


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

  return render(request, 'users/editlisting.html', context)



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

    return render(request, 'users/archived.html', context)

@login_required
def forested(request, listing_id):
    forested = get_object_or_404(Listing, pk=listing_id)
    form = ForesterForm(request.POST or None, instance=forested)
    form.fields['forester'].queryset = Contact.objects.all().filter(user_id=request.user.id)

    context = {
        'forested': forested,
        "form": form,
    }


    if request.method == "POST":
      form = ForesterForm(request.POST, instance=forested)
      if form.is_valid():
          form = form.save(commit=False)
          form.adstatus_id = get_object_or_404(Adstatus, pk=4)
          form.save()
          return redirect('posts')
      else:
          form = ForesterForm(instance=forested)

    return render(request, 'users/forested.html', context)


@login_required
def contacts(request):
    contacts = Contact.objects.filter(user_id=request.user.id).order_by('-created')


    if 'delete' in request.POST:
        id_list = request.POST.getlist('instance')
        if id_list:
            for i in id_list:
                contacts = Contact.objects.filter(id=i)
                for object in contacts:
                    object.delete()
                    return redirect('contacts')
        else:
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
        writer.writerow(['Name', 'Listing', 'Type', 'Group', 'Phone', 'Address', 'Links', 'Comments', 'Created'])

        for contact in Contact.objects.all().filter(user_id=request.user.id).values_list('name', 'listing__title', 'type__title', 'group', 'phone', 'address', 'links', 'comments', 'created'):
            writer.writerow(contact)

        return response

    if 'export_ru' in request.POST:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Export_Contacts.csv"'
        response.write(u'\ufeff'.encode('utf8'))

        writer = csv.writer(response, delimiter=',')
        writer.writerow(['Имя', 'Объявление', 'Тип владельца', 'Группа', 'Телефон', 'Адрес', 'Ссылки', 'Комментарии', 'Дата создания'])

        for contact in Contact.objects.all().filter(user_id=request.user.id).values_list('name', 'listing__title', 'type__title_ru', 'group', 'phone', 'address', 'links', 'comments', 'created'):
            writer.writerow(contact)

        return response


    paginator = Paginator(contacts, 5)
    page = request.GET.get('page')
    paged_contacts = paginator.get_page(page)


    context = {
     'contacts': paged_contacts
     }


    return render(request, 'users/responsible.html', context)


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

    return render(request, 'users/newcontact.html', context)

@login_required
def editcontact(request, contact_id):
    archived = Listing.objects.all().filter(user_id=request.user.id).exclude(adstatus_id_id = '3')
    editcontact = Contact.objects.get(pk=contact_id)
    types = Contactstype.objects.all()
    groups = Contactsgroup.objects.all()
    listings = Listing.objects.filter(user_id=request.user.id)

    context = {
    'types': types,
    'groups': groups,
    'editcontact': editcontact,
    'archived': archived,
    'listings': listings
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


    if 'attach' in request.POST:
        id_list = request.POST.getlist('instance')
        if id_list:
            for i in id_list:
                archived = get_object_or_404(Listing, pk=i)
                editcontact.attached = archived
                editcontact.save()
                return redirect('contacts')
        else:
            return redirect('editcontact')

    # if 'detach' in request.POST:
    #     id_list = request.POST.getlist('instance')
    #     if id_list:
    #         for i in id_list:
    #             archived = get_object_or_404(Listing, pk=i)
    #             editcontact = get_object_or_404(Contact, pk=contact_id)
    #             if archived.owner_id == editcontact.id:
    #                 archived.owner_id = None
    #                 archived.save()
    #                 return redirect('contacts')
    #             else:
    #                 messages.error(request, 'The listing does not belong to this Contact')
                    # return redirect('contacts')

    return render(request, 'users/editcontact.html', context)
