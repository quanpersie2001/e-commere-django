from django.db import models

from user.models import CustomerUser

# Create your models here.

STATUS = (
    ('p', 'Pending'),
    ('ds', 'Delivered to shipper'),
    ('c', 'Complete'),
    ('cc', 'Cancel')
)

PAYMENT_TYPE = (
    ('PD', 'Payment on delivery'),
    ('PP', 'Paypal')
)


class Order(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, editable=False)
    order_description = models.TextField(null=True, blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS, max_length=50, default='p')
    total_price = models.FloatField(max_length=50, null=True)

    # Sẽ có các phương thức thanh toán, được thực hiện sau này
    # payment_type = models.CharField(choices=PAYMENT_TYPE, max_length=50)
    # paid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.id} | {self.user.username}'

    @property
    def address(self):
        return self.address.all()[0]


class ShippingAddress(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.SET_NULL, null=True)
    order = models.OneToOneField(Order, on_delete=models.SET_NULL, null=True, related_name='address')
    phone_number = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    country = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.phone_number}, {self.address}, {self.state}, {self.city}, {self.country}'
