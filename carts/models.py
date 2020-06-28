from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL
from django.db.models.signals import pre_save, post_save, m2m_changed
from products.models import Product
from listings.models import Listing

class CartManager(models.Manager):

    def new_or_get(self, request):
        cart_id = request.session.get('cart_id', None)
        qs = self.get_queryset().filter(id=cart_id)
        if request.user.is_authenticated:
            user_carts = self.model.objects.filter(user=request.user)
            if user_carts.exists():
                new_obj = False
                cart_obj = user_carts.first()
                if cart_obj.user is None:
                    cart_obj.user = request.user
                    cart_obj.save()
            else:
                cart_obj = self.model.objects.create(user=request.user)
                new_obj = True
                request.session['cart_id'] = cart_obj.id
        else:
            if qs.count() == 1:
                new_obj = False
                cart_obj = qs.first()
            else:
                cart_obj = self.model.objects.create(user=None)
                new_obj = True
                request.session['cart_id'] = cart_obj.id

        return cart_obj, new_obj


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    listings = models.ManyToManyField(Listing, blank=True)
    subtotal = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

def m2m_changed_cart_receiver(sender, instance, action, *args ,**kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        listings = instance.listings.all()
        total = 0
        for x in listings:
            total += x.price
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()

m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.listings.through)


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        instance.total = instance.subtotal #+ 10
    else:
        instance.total = 0.00

pre_save.connect(pre_save_cart_receiver, sender=Cart)



class CartItemQuerySet(models.query.QuerySet):
    def select_active(self):
        return self.filter(product__adstatus_id = '2')

class CartItemManager(models.Manager):
    def get_queryset(self):
        return CartItemQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().select_active()

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    objects = CartItemManager()

    class Meta:
        db_table = 'CartItem'

    def sub_total(self):
        return self.product.price * self.quantity

    def __int__(self):
        return self.product
