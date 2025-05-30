from django.db import models
from django.db.models.signals import pre_save, post_save
from products.utils import unique_slug_generator
from django.urls import reverse
from blog.models import Post


class Tag(models.Model):
    title = models.CharField(max_length=120)
    title_ru = models.CharField(max_length=120)
    slug = models.SlugField()
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    posts = models.ManyToManyField(Post, blank=True)

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse('post-by-tag', args=[self.slug])


def tag_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(tag_pre_save_receiver, sender=Tag)
