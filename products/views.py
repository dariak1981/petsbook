from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Product, ProductCategory
from listings.models import Listing
from pages.models import Services
from analysis.mixins import ObjectViewedMixin
from carts.models import Cart, CartItem

class ProductListView(ListView):
    template_name = 'products/list.html'
    context_object_name = 'object_list'
    paginate_by = 9

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        context['category_links'] = ProductCategory.objects.all()
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all_active()


class ProductCategoryView(ListView):
    template_name = 'products/list.html'
    context_object_name = 'object_list'
    paginate_by = 9

    def get_context_data(self, *args, **kwargs):
        context = super(ProductCategoryView, self).get_context_data(*args, **kwargs)
        context['category_links'] = ProductCategory.objects.all()
        q = self.kwargs.get('category_slug')
        context['categories'] = ProductCategory.objects.filter(slug=q).first()
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('category_slug')
        return Product.objects.get_by_category(slug)


class ProductDetailSlugView(ObjectViewedMixin, DetailView):
    queryset = Product.objects.all_active()
    template_name = 'products/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        items_wishlisted = CartItem.objects.filter(cart=cart_obj)
        q = self.kwargs.get('slug')
        wishlisted = items_wishlisted.filter(product__slug=q)
        context['wishlisted'] = wishlisted
        context['services'] = Services.objects.all()
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            instance = Product.objects.all_active().get(slug=slug)
        except Product.DoesNotExist:
            raise Http404('Not found...')
        except Product.MultipleObjectsReturned:
            qs = Product.objects.all_active().filter(slug=slug)
            instance = qs.first()
        except:
            raise Http404('Uhhmmmm ')
        return instance

class ProductSearchView(ListView):
    template_name = 'products/search.html'
    paginate_by = 9

    def get_context_data(self, *args, **kwargs):
        context = super(ProductSearchView, self).get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q')
        context['category_links'] = ProductCategory.objects.all()
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None)
        if query is not None:
            return Product.objects.search(query)
        return Product.objects.all_active()
