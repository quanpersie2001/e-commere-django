from django.contrib import admin
from .models import Image, Product, Category


# Register your models here.
class ProductImageAdmin(admin.StackedInline):
    model = Image
    extra = 0
    min_num = 3


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]

    class Meta:
        model = Product


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)