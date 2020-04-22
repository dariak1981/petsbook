from django import forms
from .models import *


# class Typebreeds(forms.ModelForm):
#
#     def __init__(self, *args, **kwargs):
#         super(Typebreeds, self).__init__(*args, **kwargs)
#         self.fields['types_id'].choices = list(Taps.objects.values_list('id', 'title'))
#
#         self.fields['breed'].choices = list(Breeds.objects.values_list('id', 'title'))
#
#
#     class Meta:
#         Model: Listing
