import os
from uuid import uuid4

from django.db import models
from product.models import Product, Category


# Create your models here.


def path_and_rename(instance, filename):
    upload_to = 'home_images'
    ext = filename.split('.')[-1]
    # set filename as random string
    filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class Banner(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_transparent_bg = models.ImageField(upload_to=path_and_rename)
    short_descriptions = models.TextField(max_length=300, default='')

    def __str__(self):
        return f'{self.product.title} Banner'


class FeatureCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, unique=True)
    transparent_image = models.ImageField(upload_to=path_and_rename)


class Awesome(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, unique=True)
