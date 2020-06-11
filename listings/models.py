from django.db import models
from datetime import date, datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
import pytz
from PIL import Image
from django.utils.translation import gettext_lazy as _


class ImageField(models.ImageField):

    def save_form_data(self, instance, data):
     if data is not None:
         file = getattr(instance, self.attname)
         if file != data:
             file.delete(save=False)
     super(ImageField, self).save_form_data(instance, data)


from users.models import Contact

class Category(models.Model):
    title = models.CharField(max_length=70)
    title_ru = models.CharField(max_length=70)
    def __str__(self):
        return self.title


class Taps(models.Model):
    title = models.CharField(max_length=70)
    title_ru = models.CharField(max_length=70)
    def __str__(self):
        return self.title


class Breeds(models.Model):
    type_id = models.ForeignKey(Taps, on_delete=models.CASCADE)
    title = models.CharField(max_length=70)
    title_ru = models.CharField(max_length=70)
    def __str__(self):
        return self.title


class Gender(models.Model):
    title = models.CharField(max_length=70)
    title_ru = models.CharField(max_length=70)
    def __str__(self):
        return self.title

class Age(models.Model):
    title = models.CharField(max_length=150)
    title_ru = models.CharField(max_length=150)
    def __str__(self):
        return self.title

class Condition(models.Model):
    title = models.CharField(max_length=70)
    title_ru = models.CharField(max_length=70)
    def __str__(self):
        return self.title

class Health(models.Model):
    title = models.CharField(max_length=200)
    title_ru = models.CharField(max_length=200)
    def __str__(self):
        return self.title

class Adstatus(models.Model):
    title = models.CharField(max_length=200)
    def __str__(self):
        return self.title


class Listing(models.Model):



    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name= _('created'),)
    user_contact = models.CharField(max_length=150, verbose_name = _('contacts'),)
    title = models.CharField(max_length=100, verbose_name= _('title'),)
    category_id = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name= _('category'),)
    types_id = models.ForeignKey(Taps, on_delete=models.CASCADE, verbose_name = _('type'),)
    city = models.CharField(max_length=20, verbose_name= _('city'),)
    district = models.CharField(max_length=30, verbose_name= _('district'),)
    price = models.IntegerField(verbose_name= _('price'),)
    breeds = models.ForeignKey(Breeds, on_delete=models.DO_NOTHING, verbose_name= _('breeds'),)
    age_id = models.ForeignKey(Age, on_delete=models.DO_NOTHING, verbose_name = _('age'),)
    gender_id = models.ForeignKey(Gender, on_delete=models.DO_NOTHING, verbose_name = _('gender'),)
    conditions_id = models.ForeignKey(Condition, on_delete=models.DO_NOTHING, verbose_name = _('conditions'),)
    health_id = models.ForeignKey(Health, on_delete=models.DO_NOTHING, verbose_name = _('health'),)
    video = models.CharField(max_length=300, blank=True, verbose_name= _('youtube'),)
    description = models.TextField(max_length=2500, blank=True, verbose_name= _('description'),)
    created = models.DateTimeField(default=timezone.now, blank=True, verbose_name= _('created'),)
    archived = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    adstatus_id = models.ForeignKey(Adstatus, on_delete=models.DO_NOTHING, default='1')
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name = _('main photo'),)
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name= _('photo_1'),)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name= _('photo_2'),)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name= _('photo_3'),)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name= _('photo_4'),)
    owner = models.ForeignKey(Contact, on_delete=models.DO_NOTHING, default=None, blank=True, null=True, verbose_name= _('owner'), related_name='listing_owner',)
    forester = models.ForeignKey(Contact, on_delete=models.DO_NOTHING, default=None, blank=True, null=True, verbose_name= _('forester'), related_name='listing_foster',)
    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        super(Listing, self).save(*args, **kwargs)

        if self.photo_main:

            img = Image.open(self.photo_main.path)

            if img.height > 1000 or img.width > 1000:
                output_size = (1000, 1000)
                img.thumbnail(output_size)
                img.save(self.photo_main.path)

        if self.photo_1:

            img = Image.open(self.photo_1.path)

            if img.height > 1100 or img.width > 1100:
                output_size = (1100, 1100)
                img.thumbnail(output_size)
                img.save(self.photo_1.path)

        if self.photo_2:

            img = Image.open(self.photo_2.path)

            if img.height > 1000 or img.width > 1000:
                output_size = (1000, 1000)
                img.thumbnail(output_size)
                img.save(self.photo_2.path)

        if self.photo_3:

            img = Image.open(self.photo_3.path)

            if img.height > 1000 or img.width > 1000:
                output_size = (1000, 1000)
                img.thumbnail(output_size)
                img.save(self.photo_3.path)

        if self.photo_4:

            img = Image.open(self.photo_4.path)

            if img.height > 1000 or img.width > 1000:
                output_size = (1000, 1000)
                img.thumbnail(output_size)
                img.save(self.photo_4.path)
