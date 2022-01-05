from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from product.models import Category, Product
from home.models import Banner, FeatureCategory, FeatureCategory, Awesome


# Create your views here.

class HomeView(View):
    def get(self, request):
        context = {
            'awesome': Awesome.objects.all(),
            'featureCategories': FeatureCategory.objects.all(),
            'categories': Category.objects.all(),
            'products': Product.objects.all(),
            'banners': Banner.objects.all(),
            'range': range(len(Awesome.objects.all()) // 8 + 1),
        }
        return render(request, 'homepage/index.html', context)


class ShopView(ListView):
    model = Product
    template_name = 'shop/shop.html'

    def get(self, request):
        context = {
            'categories': Category.objects.all(),
            'products': Product.objects.all(),
        }
        return render(request, 'shop/shop.html', context)


class DetailProduct(DetailView):
    model = Product
    template_name = 'detail/detail.html'
