from .models import CartItem, Cart
from products.models import Product
from django.db.models import Count


def counter(request):
    item_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart_obj, new_obj = Cart.objects.new_or_get(request)
            cart_items = CartItem.objects.filter(cart_id=cart_obj.id)
            for cart_item in cart_items:
                item_count += cart_item.quantity
        except Cart.DoesNotExist:
            item_count = 0

    return dict(item_count = item_count)


def wishitems(request):
    items_wishlisted = []
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    items_wishlisted = CartItem.objects.all().filter(cart_id=cart_obj.id).values_list('product__id', flat=True)
    return dict(items_wishlisted = items_wishlisted)

def listingitems(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    listing_items = cart_obj.listings.count()
    return dict(listing_items = listing_items)
