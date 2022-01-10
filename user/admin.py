from django.contrib import admin
from .models import CustomerUser


# Register your models here.


class UserAdmin(admin.ModelAdmin):
    model = CustomerUser
    list_display = ('id', 'username', 'email', 'date_joined', 'is_active', 'is_staff')


admin.site.register(CustomerUser, UserAdmin)
