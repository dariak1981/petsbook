from django.db import models
from datetime import date, datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from PIL import Image


class Themes(models.Model):
    title = models.CharField(max_length=400)
    title_ru = models.CharField(max_length=400)
    def __str__(self):
        return self.title

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = _('author'),)
    title = models.CharField(max_length=100, verbose_name = _('title'),)
    is_featured = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now, blank=True, verbose_name = _('created'),)
    updated = models.DateTimeField(auto_now=True)
    theme = models.ForeignKey(Themes, on_delete=models.CASCADE, verbose_name = _('theme'),)
    content = models.TextField(max_length=20000, blank=False, verbose_name = _('content'),)
    photo = models.ImageField(upload_to='blog/%Y/%m/%d/', blank=True, verbose_name = _('photo'),)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)

        if self.photo:

            img = Image.open(self.photo.path)

            if img.height > 1000 or img.width > 1000:
                output_size = (1000, 1000)
                img.thumbnail(output_size)
                img.save(self.photo.path)

class Message(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = _('author'),)
    message = models.TextField(max_length=2500, blank=False, verbose_name = _('message'),)
    created = models.DateTimeField(default=timezone.now, verbose_name = _('created'),)
    def __int__(self):
        return self.message

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.post_id})
