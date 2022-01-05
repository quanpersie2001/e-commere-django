from django.db import models
from user.models import CustomerUser
from cart.models import Cart
# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    shipping_address = models.CharField(default='', max_length=255)
    order_description = models.TextField(default='')
    is_completed = models.BooleanField(default=False)