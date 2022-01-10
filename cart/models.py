from django.db import models
from django.utils.safestring import mark_safe

from product.models import Product
from user.models import CustomerUser
from order.models import Order


# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, related_name='cart', editable=False)
    active = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f' CartID: {self.id} | UserID: {self.user.id} | Username: {self.user.username}'

    @staticmethod
    def get_all_items(user):
        carts = Cart.objects.filter(user=user, active=True)
        if carts:
            cart = carts[0]
            return cart.cart_items.all()
        else:
            return []

    @property
    def get_total_price(self):
        items = self.cart_items.all()
        return sum([item.get_total for item in items])

    @staticmethod
    def item_quantity(user):
        if user.is_anonymous:
            return 0
        carts = Cart.objects.filter(user=user, active=True)
        if carts:
            cart = carts[0]
            return sum([item.quantity for item in cart.cart_items.all()])
        else:
            return 0


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    order = models.ForeignKey(Order, on_delete=models.RESTRICT, null=True, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return ''

    @property
    def get_total(self):
        return self.product.price * self.quantity

    def image_(self):
        if self.product.first_image():
            return mark_safe(
                '<img src="%s" style="width: 60px; height:60px;" />' % self.product.first_image().image.url)
        else:
            return 'No Image Found'

    def title_(self):
        return self.product.title

    def quantity_(self):
        return self.quantity

    def total_(self):
        return self.get_total
