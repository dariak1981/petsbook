from django import forms
from listings.models import Listing, Category
from .models import Contact
from accounts.models import Profile
from django.conf import settings
User = settings.AUTH_USER_MODEL
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.forms.widgets import FileInput


class UserForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'usertype', 'publicmail', 'business', 'phone', 'links',
            'description', 'photo'
        ]

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            'title', 'user_contact', 'category_id', 'types_id', 'city', 'district', 'price', 'breeds', 'age_id', 'gender_id',
            'conditions_id', 'health_id', 'photo_main', 'photo_1', 'photo_2', 'photo_3', 'photo_4', 'description'
        ]
        exclude = ['user']

class ArchiveForm(forms.ModelForm):

    class Meta:
        model = Listing
        fields = [
          'owner'
        ]
        exclude = ['adstatus_id']

class AttachContactsForm(forms.ModelForm):

    class Meta:
        model = Listing
        fields = [
          'forester'
        ]
        exclude = ['adstatus_id']



class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = [
            'type', 'group', 'name', 'address', 'phone', 'links', 'comments'
        ]
        exclude = ['user']
