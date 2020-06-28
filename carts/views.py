from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import Cart, CartItem
from products.models import Product
from listings.models import Listing


# def _cart_id(request):
#     cart_obj, new_obj = Cart.objects.new_or_get(request)
#     return cart_obj, new_obj

def cart_update(request):
    listing_id = request.POST.get('listing_id')
    if listing_id is not None:
        try:
            listing_obj = Listing.objects.get(id=listing_id)
        except Listing.DoesNotExist:
            print('Listing is not active')
            return redirect('carts:home')
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if listing_obj in cart_obj.listings.all():
            cart_obj.listings.remove(listing_obj)
        else:
            cart_obj.listings.add(listing_obj) #cart_obj.products.add(product_id) cart_obj.products.remove(obj)
        request.session['cart_items'] = cart_obj.listings.count()
    return redirect('carts:cart_detail')


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    try:
        cart_item = CartItem.objects.get(product=product, cart_id=cart_obj.id)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart_id=cart_obj.id
        )
        cart_item.save()

    return redirect('carts:cart_detail')


def cart_detail(request, total=0, counter=0, cart_items=None,  cart=None):
    try:
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        cart_items = CartItem.objects.active().filter(cart=cart_obj)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request, 'carts/cart.html', dict(cart=cart_obj, cart_items=cart_items, total=total, counter=counter))

def cart_remove(request, product_id):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart_obj)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('carts:cart_detail')

def cart_remove_product(request, product_id):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart_obj)
    cart_item.delete()
    return redirect('carts:cart_detail')
