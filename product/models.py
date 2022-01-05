import os
from uuid import uuid4

from django.db import models
from django.shortcuts import reverse
from autoslug import AutoSlugField


# Create your models here.
AVAILABILITY = (
    (True, 'In Stock'),
    (False, 'Out Stock'),

)


def path_and_rename(instance, filename):
    upload_to = 'product_images'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class Category(models.Model):
    title = models.CharField(default='', max_length=100, unique=True)
    slug = models.CharField(default='', max_length=100)
    description = models.TextField(default='')
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to=path_and_rename, max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(default='', max_length=100)
    description = models.TextField(default='')
    price = models.FloatField(default=0.0)
    active = models.BooleanField(choices=AVAILABILITY, default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from='title', unique=True)

    def __str__(self):
        return self.title

    def first_image(self):
        return self.images.all()[0]

    def get_absolute_url(self):
        return reverse("product", kwargs={
            'slug': self.slug
        })


class Image(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=path_and_rename, max_length=255, null=True, blank=True)

    def __str__(self):
        return self.image.url


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(default='', max_length=255)
    price = models.FloatField(default=0.0)
    sale_price = models.FloatField(default=0.0)
    active = models.BooleanField(default=True)
    inventory = models.IntegerField(default=0)

