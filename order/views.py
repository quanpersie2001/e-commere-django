import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from cart.models import Cart, CartItem
from order.models import Order


class PurchaseView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'user_order/order.html'
    login_url = '/account/log-in/'

    def get_context_data(self, **kwargs):
        orders = Order.objects.filter(user=self.request.user).order_by('-status')
        context = super().get_context_data(**kwargs)
        context['cart_quantity'] = Cart.item_quantity(self.request.user)
        context['orders'] = orders
        return context


@login_required(login_url='/account/log-in/')
def update_order(request):
    data = json.loads(request.body)
    orderId = data['orderId']
    action = data['action']

    user = request.user
    order = Order.objects.get(id=orderId)

    status = order.status

    if action == 'cancel':
        if status == 'ds':
            messages.error(request, 'Orders in transit cannot be cancelled')
        elif status == 'c':
            messages.error(request, 'Completed orders cannot be canceled')
        elif status == 'cc':
            messages.error(request, 'Canceled orders cannot be canceled')
        else:
            order.status = 'cc'
            order.save()

    return JsonResponse('Item was added', safe=False)
