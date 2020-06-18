from django.dispatch import Signal
from django.conf import settings
from django.db.models.signals import post_save

user_logged_in = Signal(providing_args=['instance','request'])

def post_save_receiver(sender, instance, created, **kwargs):
    pass

post_save.connect(post_save_receiver, sender=settings.AUTH_USER_MODEL)
