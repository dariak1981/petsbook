from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from PIL import Image
from django.utils.translation import gettext_lazy as _


class UserType(models.Model):
    title = models.CharField(max_length=100)
    title_ru = models.CharField(max_length=100)
    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    usertype = models.ForeignKey(UserType, on_delete=models.DO_NOTHING, verbose_name = _('users_group'), default='5')
    publicmail = models.CharField(max_length=100, blank=True, verbose_name = _('public email'),)
    business = models.CharField(max_length=250, blank=True, verbose_name = _('organization name'),)
    phone = models.CharField(max_length=20, blank=True, verbose_name = _('phone'),)
    links = models.CharField(max_length=70, blank=True, verbose_name = _('links'),)
    description = models.CharField(max_length=300, blank=True, verbose_name = _('details'),)
    photo = models.ImageField(upload_to='profile_pics', blank=True, verbose_name = _('photo'),)
    def __int__(self):
        return self.user


    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)

        if self.photo:

            img = Image.open(self.photo.path)

            if img.height > 500 or img.width > 500:
                output_size = (500, 500)
                img.thumbnail(output_size)
                img.save(self.photo.path)



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

# Contacts
class Contactstype(models.Model):
    title = models.CharField(max_length=100)
    title_ru = models.CharField(max_length=100)
    def __str__(self):
        return self.title

class Contactsgroup(models.Model):
    title = models.CharField(max_length=100)
    def __str__(self):
        return self.title


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(Contactstype, on_delete=models.DO_NOTHING, verbose_name = _('owner type'),)
    group = models.ForeignKey(Contactsgroup, on_delete=models.DO_NOTHING, verbose_name = _('group'),)
    name = models.CharField(max_length=150, verbose_name = _('name'),)
    address = models.CharField(max_length=100, blank=True, verbose_name = _('address'),)
    phone = models.CharField(max_length=20, blank=True, verbose_name = _('phone'),)
    links = models.CharField(max_length=250, blank=True, verbose_name = _('links'),)
    comments = models.TextField(max_length=2500, blank=True, verbose_name = _('comments'),)
    created = models.DateTimeField(default=datetime.now, verbose_name = _('created'),)
    def __str__(self):
        return self.name
