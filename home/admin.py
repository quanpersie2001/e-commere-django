from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from .models import Banner, FeatureCategory


# Register your models here.


class BannerAdmin(admin.ModelAdmin):
    def add_view(self, request, form_url='', extra_context=None):
        if self.model.objects.count() >= 4:
            self.message_user(request, 'Only four banners can exist at once - please remove others first',
                              messages.ERROR)
            return HttpResponseRedirect(reverse(f'admin:{self.model._meta.app_label}_banner_changelist'))
        return super().add_view(request, form_url, extra_context)


class FeatureCategoryAdmin(admin.ModelAdmin):
    def add_view(self, request, form_url='', extra_context=None):
        if self.model.objects.count() >= 4:
            self.message_user(request, 'Only four category can exist at once - please remove others first',
                              messages.ERROR)
            return HttpResponseRedirect(reverse(f'admin:{self.model._meta.app_label}_feature_category_changelist'))
        return super().add_view(request, form_url, extra_context)


admin.site.register(Banner, BannerAdmin)
admin.site.register(FeatureCategory, FeatureCategoryAdmin)
