from django.contrib import admin
from .models import Order
from cart.models import CartItem


# Register your models here.

class OderItemAdmin(admin.TabularInline):
    model = CartItem
    fields = ['image_', 'title_', 'quantity_', 'total_']
    readonly_fields = ['image_', 'title_', 'quantity_', 'total_']


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ('id', 'get_username', 'get_address', 'get_total_price', 'time_create', 'status',)
    inlines = [OderItemAdmin, ]

    @admin.display(description='Address')
    def get_address(self, obj):
        return obj.address

    @admin.display(description='Username')
    def get_username(self, obj):
        return obj.user.username

    @admin.display(description='Total Price')
    def get_total_price(self, obj):
        return obj.total_price


admin.site.register(Order, OrderAdmin)
