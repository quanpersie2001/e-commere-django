import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from django.utils import timezone
from django.views.generic import ListView

from cart.models import Cart, CartItem
from product.models import Product
# Create your views here.


class CartView(LoginRequiredMixin, ListView):
    login_url = '/account/log-in/'
    template_name = 'cart/cart.html'

    def get(self, request):
        cart_items = Cart.get_all_items(request.user)
        cart_qs = Cart.objects.filter(user=request.user, active=True)
        cart_quantity = Cart.item_quantity(request.user)
        if cart_qs.exists():
            cart = cart_qs[0]
        else:
            cart = None
        context = {
            'cart_items': cart_items,
            'cart': cart,
            'cart_quantity': cart_quantity,
        }
        return render(request, self.template_name, context)


@login_required(login_url='/account/log-in/')
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart_qs = Cart.objects.filter(user=request.user, active=True)
    if cart_qs.exists():
        cart = cart_qs[0]
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            cart=cart,
        )
        # check if the cart item is in the cart
        if cart.cart_items.filter(product__slug=product.slug).exists():
            cart_item.quantity += 1
            cart_item.save()
            info_msg = 'This item quantity was updated.'
        else:
            cart.cart_items.add(cart_item)
            info_msg = 'This item was added to your cart.'
    else:
        created_date = timezone.now()
        cart = Cart.objects.create(user=request.user, create_at=created_date)
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            cart=cart,
        )
        cart.cart_items.add(cart_item)
        info_msg = 'This item was added to your cart.'
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def update_cart(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    user = request.user
    product = Product.objects.get(id=productId)
    cart, created = Cart.objects.get_or_create(user=user, active=True)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if action == 'add':
        cart_item.quantity = (cart_item.quantity + 1)
    elif action == 'remove':
        if cart_item.quantity == 1:
            pass
        else:
            cart_item.quantity = (cart_item.quantity - 1)

    cart_item.save()

    if action == 'delete':
        cart_item.delete()

    return JsonResponse('Order was added', safe=False)
