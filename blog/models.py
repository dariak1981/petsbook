from django.db import models
from datetime import date, datetime
from django.conf import settings
User = settings.AUTH_USER_MODEL
from django.utils import timezone
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from PIL import Image
from django.db.models import Q
from functools import reduce
import operator
from django.db.models.signals import pre_save, post_save
from products.utils import unique_slug_generator
from django.urls import reverse


class Themes(models.Model):
    slug = models.SlugField(max_length=400, unique=True)
    title = models.CharField(max_length=400)
    title_ru = models.CharField(max_length=400)

    class Meta:
        verbose_name = 'theme'
        verbose_name_plural = 'themes'

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse('category-view', args=[self.slug])

def category_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(category_pre_save_receiver, sender=Themes)

class PostQuerySet(models.query.QuerySet):

    def search(self, query):
        term_list = query.split(' ')

        query = reduce(operator.and_,
            ((Q(title__icontains=item) |
            Q(author_id__username__icontains=item) |
            Q(content__icontains=item) |
            Q(theme_id__title__icontains=item) |
            Q(theme_id__title_ru__icontains=item) |
            Q(tag__title__icontains=item) |
            Q(tag__title_ru__icontains=item))
            for item in term_list))
        return self.filter(query).distinct()


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def get_by_category(self, category_slug):
        qs =  self.get_queryset().filter(theme_id__slug__iexact=category_slug)
        return qs

    def get_by_tag(self, tag_slug):
        qs =  self.get_queryset().filter(tag__slug__icontains=tag_slug)
        return qs

    def search(self, query):
        return self.get_queryset().search(query)

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name = _('author'),)
    slug = models.SlugField(max_length=120, unique=True)
    title = models.CharField(max_length=100, verbose_name = _('title'),)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='post_likes')
    is_featured = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now, blank=True, verbose_name = _('created'),)
    updated = models.DateTimeField(auto_now=True)
    theme = models.ForeignKey(Themes, on_delete=models.CASCADE, verbose_name = _('theme'),)
    content = models.TextField(max_length=20000, blank=False, verbose_name = _('content'),)
    photo = models.ImageField(upload_to='blog/%Y/%m/%d/', blank=True, verbose_name = _('photo'),)

    objects = PostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})

    def get_like_url(self):
        return reverse('like-toggle', kwargs={'slug': self.slug})


    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)

        if self.photo:

            img = Image.open(self.photo.path)

            if img.height > 1000 or img.width > 1000:
                output_size = (1000, 1000)
                img.thumbnail(output_size)
                img.save(self.photo.path)
    class Meta:
        ordering = ['-created']
        verbose_name = 'post'
        verbose_name_plural = 'posts'

def post_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(post_pre_save_receiver, sender=Post)

class Message(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name = _('author'),)
    message = models.TextField(max_length=1500, blank=False, verbose_name = _('message'),)
    created = models.DateTimeField(default=timezone.now, verbose_name = _('created'),)
    def __int__(self):
        return self.message

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.post.slug})

    class Meta:
        ordering = ['-created']
        verbose_name = 'message'
        verbose_name_plural = 'messages'
