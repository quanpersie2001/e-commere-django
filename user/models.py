from django.db import models
from django.contrib.auth.models import AbstractUser, User


# Create your models here.

class CustomerUser(AbstractUser):
    phone_number = models.CharField(default='', max_length=15)
    address = models.CharField(default='', max_length=255)
    company = models.CharField(default='', max_length=255, null=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
