from django.contrib import admin
from cart.models import Cart, CartItem


# Register your models here.

class CartItemAdmin(admin.TabularInline):
    model = CartItem
    fields = ['image_', 'title_', 'quantity_', 'total_']
    readonly_fields = ['image_', 'title_', 'quantity_', 'total_']


class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_display = ('id', 'get_user_id', 'get_username', 'create_at', 'active')
    inlines = [CartItemAdmin, ]

    @admin.display(ordering='user__id', description='UserID')
    def get_user_id(self, obj):
        return obj.user.id

    @admin.display(description='Username')
    def get_username(self, obj):
        return obj.user.username


admin.site.register(Cart, CartAdmin)
