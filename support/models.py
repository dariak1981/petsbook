from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Guidance(models.Model):
    title_ru = models.CharField(max_length=200, verbose_name= _('title'),)
    title = models.CharField(max_length=200, verbose_name= _('title eng'),)
    content_ru = models.TextField(max_length=3000, blank=True, verbose_name= _('content'),)
    content = models.TextField(max_length=3000, blank=True, verbose_name= _('content eng'),)

    def __str__(self):
        return self.title_ru


class Intro(models.Model):
    title_ru = models.CharField(max_length=100, verbose_name= _('title'),)
    title = models.CharField(max_length=100, verbose_name= _('title eng'),)
    content_ru = models.TextField(max_length=2000, blank=True, verbose_name= _('content'),)
    content = models.TextField(max_length=2000, blank=True, verbose_name= _('content eng'),)

    def __str__(self):
        return self.title_ru
