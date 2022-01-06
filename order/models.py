from django.db import models
from user.models import CustomerUser
from cart.models import Cart

# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    order_description = models.TextField(default='')
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.name


class ShippingAddress(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
