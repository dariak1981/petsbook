from django import forms
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Product, ProductCategory
from listings.models import Adstatus
User = get_user_model()

class ProductForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    class Meta:
        model = Product
        fields = ('user_contact', 'title', 'price', 'city', 'description', 'photo_main', 'photo_1', 'photo_2', 'photo_3')

class ProductCategoryForm(forms.ModelForm):

    class Meta:
        model = ProductCategory
        fields = ('id', 'title', 'title_ru')
