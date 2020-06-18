from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from django.db.models import Q
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.conf import settings
User = settings.AUTH_USER_MODEL
from PIL import Image
from .signals import post_save_receiver
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import get_template
from .utils import random_string_generator, unique_key_generator

DEFAULT_ACTIVATION_DAYS = getattr(settings, 'DEFAULT_ACTIVATION_DAYS', 7)

class UserManager(BaseUserManager):
    def create_user(self, email, username, full_name, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        if not username:
            raise ValueError("Users must have username")
        if not full_name:
            raise ValueError("Users must have a full name")


        user_obj = self.model(
            email = self.normalize_email(email),
            username = username,
            full_name = full_name,
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, username, full_name, password=None):
        user = self.create_user(
            email,
            username,
            full_name,
            password=password,
            is_staff=True,
        )
        return user

    def create_superuser(self, email, username, full_name, password=None):
        user = self.create_user(
            email,
            username,
            full_name,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        return user

class User(AbstractBaseUser):
    # username = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True) # can login
    staff = models.BooleanField(default=False) # staff user non superuser
    admin = models.BooleanField(default=False) # superuser
    joined = models.DateTimeField(auto_now_add=True, blank=True, null=True)


    USERNAME_FIELD = 'email' #username
    REQUIRED_FIELDS = ['username','full_name']

    objects = UserManager()



    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    # @property
    # def is_active(self):
    #     return self.active

    @property
    def is_staff(self):
        return self.staff

class UserType(models.Model):
    title = models.CharField(max_length=100)
    title_ru = models.CharField(max_length=100)
    def __str__(self):
        return self.title

class Profile(models.Model):
        user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, blank=True, related_name='profile',)
        usertype = models.ForeignKey(UserType, on_delete=models.DO_NOTHING, verbose_name = _('users_group'), default='5')
        publicmail = models.CharField(max_length=100, blank=True, verbose_name = _('blog email'),)
        business = models.CharField(max_length=250, blank=True, verbose_name = _('organization name'),)
        phone = models.CharField(max_length=20, blank=True, verbose_name = _('phone'),)
        links = models.CharField(max_length=70, blank=True, verbose_name = _('links'),)
        description = models.CharField(max_length=300, blank=True, verbose_name = _('details'),)
        photo = models.ImageField(upload_to='profile_pics', blank=True, verbose_name = _('photo'),)
        ad_organization = models.CharField(max_length=200, blank=True, verbose_name = _('organization'),)
        ad_address = models.CharField(max_length=200, blank=True, verbose_name = _('company address'),)
        ad_website = models.CharField(max_length=200, blank=True, verbose_name = _('website'),)
        ad_email = models.CharField(max_length=150, blank=True, verbose_name = _('company email'),)
        ad_youtube = models.CharField(max_length=200, blank=True)
        ad_facebook = models.CharField(max_length=200, blank=True)
        ad_vk = models.CharField(max_length=200, blank=True)
        def __int__(self):
            return self.user


        def save(self, *args, **kwargs):
            super(Profile, self).save(*args, **kwargs)

            if self.photo:

                img = Image.open(self.photo.path)

                if img.height > 500 or img.width > 500:
                    output_size = (500, 500)
                    img.thumbnail(output_size)
                    img.save(self.photo.path)



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class EmailActivationQuerySet(models.query.QuerySet):
    def confirmable(self):
        now = timezone.now()
        start_range = now - timedelta(days=DEFAULT_ACTIVATION_DAYS)
        end_range = now
        return self.filter(
            activated=False,
            forced_expired=False
        ).filter(
          timestamp__gt=start_range,
          timestamp__lte=end_range
        )

class EmailActivationManager(models.Manager):
    def get_queryset(self):
        return EmailActivationQuerySet(self.model, using=self._db)

    def confirmable(self):
        return self.get_queryset().confirmable()

    def email_exists(self, email):
        return self.get_queryset().filter(
                Q(email=email) | Q(user__email=email)
            ).filter(
                activated=False
            )


class EmailActivation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    key = models.CharField(max_length=120, blank=True, null=True)
    activated = models.BooleanField(default=False)
    forced_expired = models.BooleanField(default=False)
    expires = models.IntegerField(default=7) #7 days
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    objects = EmailActivationManager()

    def __str__(self):
        return self.email

    def can_activate(self):
        qs = EmailActivation.objects.filter(pk=self.pk).confirmable() # 1 object
        if qs.exists():
            return True
        return False

    def activate(self):
        if self.can_activate():
            # pre activation signal
            user=self.user
            user.is_active=True
            user.save()
            # post activation signal
            self.activated=True
            self.save()
            return True
        return False

    def regenerate(self):
        self.key = None
        self.save()
        if self.key is not None:
            return True
        return False

    def send_activation(self):
        if not self.activated and not self.forced_expired:
            if self.key:
                base_url = getattr(settings, 'BASE_URL', 'https://www.petsbook.club/')
                key_path = reverse('email-activate', kwargs={'key':self.key})
                path = '{base}{path}'.format(base=base_url,path=key_path)
                context = {
                    'path': path,
                    'email': self.email
                }

                txt_ = get_template('accounts/emails/verify.txt').render(context)
                html_ = get_template('accounts/emails/verify.html').render(context)
                subject = '1-Click Email Verification'
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [self.email]
                sent_mail = send_mail(
                        subject,
                        txt_,
                        from_email,
                        recipient_list,
                        html_message=html_,
                        fail_silently=False,
                    )
                return sent_mail
        return False


def pre_save_email_activation(sender, instance, *args, **kwargs):
    if not instance.activated and not instance.forced_expired:
        if not instance.key:
            instance.key = unique_key_generator(instance)

pre_save.connect(pre_save_email_activation, sender=EmailActivation)

def post_save_user_create_receiver(sender, instance, created, *args, **kwargs):
    if created:
        obj = EmailActivation.objects.create(user=instance, email=instance.email)
        obj.send_activation()

post_save.connect(post_save_user_create_receiver, sender=User)
