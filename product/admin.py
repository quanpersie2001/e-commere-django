from django.contrib import admin
from .models import Image, Product, Category


# Register your models here.
class ProductImageAdmin(admin.TabularInline):
    model = Image
    # fields = ['image_tag', ]
    readonly_fields = ['image_tag', ]


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('id', 'title', 'category', 'price', 'quantity', 'status', 'active', 'image_tag')
    inlines = [ProductImageAdmin, ]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
