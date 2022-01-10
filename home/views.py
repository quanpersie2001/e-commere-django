from django.shortcuts import render

# Create your views here.
from django.views import View

from cart.models import Cart
from home.models import Awesome, FeatureCategory, Banner
from product.models import Category, Product


class HomeView(View):
    template_name = 'homepage/index.html'

    def get(self, request):
        cart_quantity = Cart.item_quantity(request.user)
        context = {
            'awesome': Awesome.get_all_awesome(),
            'featureCategories': FeatureCategory.get_all_feature_cate(),
            'categories': Category.get_all_category(),
            'products': Product.get_all_product(),
            'banners': Banner.get_all_banner(),
            'range': range(len(Awesome.get_all_awesome()) // 8 + 1),
            'cart_quantity': cart_quantity,
        }
        return render(request, self.template_name, context)
