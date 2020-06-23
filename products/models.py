from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL
from django.utils import timezone
from PIL import Image
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save, post_save
from .utils import unique_slug_generator
from django.urls import reverse
from django.db.models import Q
from functools import reduce
import operator

class ImageField(models.ImageField):

    def save_form_data(self, instance, data):
     if data is not None:
         file = getattr(instance, self.attname)
         if file != data:
             file.delete(save=False)
     super(ImageField, self).save_form_data(instance, data)

class ProductCategory(models.Model):
    slug = models.SlugField(max_length=70, unique=True)
    title = models.CharField(max_length=70)
    title_ru = models.CharField(max_length=70)
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products:category-view', args=[self.slug])

class Adstatus(models.Model):
    title = models.CharField(max_length=200)
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'ad status'
        verbose_name_plural = 'ad statuses'

class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(adstatus_id = '2').order_by('-created')


    def search(self, query):
        term_list = query.split(' ')

        query = reduce(operator.and_,
            ((Q(title__icontains=item) |
            Q(description__icontains=item) |
            Q(price__iexact=item) |
            Q(city__icontains=item) |
            Q(category_id__title__icontains=item) |
            Q(category_id__title_ru__icontains=item))
            for item in term_list))
        return self.filter(query).distinct()


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all_active(self):
        return self.get_queryset().active()

    def get_by_id(self, id):
        qs =  self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def get_by_category(self, category_slug):
        # category_slug = kwargs.get('category_slug')
        # category = ProductCategory.objects.filter(slug=category_slug)
        qs =  self.get_queryset().filter(category_id__slug__iexact=category_slug)
        return qs.active()


    def search(self, query):
        return self.get_queryset().active().search(query)


class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name= _('created'),)
    user_contact = models.CharField(max_length=150, verbose_name = _('contacts'),)
    adstatus_id = models.ForeignKey(Adstatus, on_delete=models.DO_NOTHING, default='1')
    category_id = models.ForeignKey(ProductCategory, on_delete=models.DO_NOTHING, verbose_name= _('category'),)
    title = models.CharField(max_length=200, verbose_name= _('title'),)
    slug =  models.SlugField(max_length=200, blank=True, null=True, unique=True)
    price = models.IntegerField(verbose_name= _('price'),)
    city = models.CharField(max_length=20, verbose_name= _('city'),)
    description = models.TextField(max_length=1500, blank=True, verbose_name= _('description'),)
    created = models.DateTimeField(default=timezone.now, blank=True, verbose_name= _('created'),)
    featured = models.BooleanField(default=False)
    photo_main = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True, null=True, verbose_name = _('main photo'),)
    photo_1 = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True, null=True, verbose_name= _('photo_1'),)
    photo_2 = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True, null=True, verbose_name= _('photo_2'),)
    photo_3 = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True, null=True, verbose_name= _('photo_3'),)
    photo_4 = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True, null=True, verbose_name= _('photo_4'),)

    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # return '/products/{slug}'.format(slug=self.slug)
        return reverse('products:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)

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

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(product_pre_save_receiver, sender=Product)
