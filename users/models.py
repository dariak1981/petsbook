from django.db import models
from datetime import datetime
from django.utils import timezone
from django.conf import settings
User = settings.AUTH_USER_MODEL
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from django.utils.translation import gettext_lazy as _



# Contacts
class Contactstype(models.Model):
    title = models.CharField(max_length=100)
    title_ru = models.CharField(max_length=100)
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'contact type'
        verbose_name_plural = 'contact types'

class Contactsgroup(models.Model):
    title = models.CharField(max_length=100)
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'contact group'
        verbose_name_plural = 'contact groups'


class Contact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.ForeignKey(Contactstype, on_delete=models.DO_NOTHING, verbose_name = _('owner type'),)
    group = models.ForeignKey(Contactsgroup, on_delete=models.DO_NOTHING, verbose_name = _('group'),)
    name = models.CharField(max_length=150, verbose_name = _('name'),)
    address = models.CharField(max_length=100, blank=True, verbose_name = _('address'),)
    phone = models.CharField(max_length=20, blank=True, verbose_name = _('phone'),)
    links = models.CharField(max_length=250, blank=True, verbose_name = _('links'),)
    comments = models.TextField(max_length=2500, verbose_name = _('comments'),)
    created = models.DateTimeField(default=datetime.now, verbose_name = _('created'),)

    def __str__(self):
        return self.name
