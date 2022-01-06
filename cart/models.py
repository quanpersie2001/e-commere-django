from django.db import models
from product.models import Product
from user.models import CustomerUser


# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f' {self.id} - {self.user.name}'

    def get_all_items(self):
        return self.cart_items.all()

    def get_total_price(self):
        return sum([t_price for t_price in self.get_all_items()])


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0)

    def get_total(self):
        return self.product.price * self.quantity
