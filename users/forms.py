from django import forms
from listings.models import Listing, Category
from .models import Contact, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.forms.widgets import FileInput

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=15, label=_(u'Username'))
    email = forms.EmailField(max_length=30)
    first_name = forms.CharField(max_length=15, label=_(u'First name'))
    last_name = forms.CharField(max_length=20, label=_(u'Last name'))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = _('Something pretty enough')
        self.fields['password2'].help_text = _('At least 8 symbols')


class UserMainForm(forms.ModelForm):
    username = forms.CharField(max_length=15, label=_(u'Username'))
    email = forms.EmailField(max_length=30)
    first_name = forms.CharField(max_length=15, label=_(u'First name'))
    last_name = forms.CharField(max_length=20, label=_(u'Last name'))

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name'
        ]

class UserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
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


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'type', 'group', 'name', 'address', 'phone', 'links', 'comments'
        ]
        exclude = ['user', 'listing_id']
