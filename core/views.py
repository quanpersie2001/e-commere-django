from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from product.models import Category, Product
from home.models import Banner, FeatureCategory, FeatureCategory, Awesome
from cart.models import Cart, CartItem


# Create your views here.

class HomeView(View):

    def get(self, request):
        context = {
            'awesome': Awesome.get_all_awesome(),
            'featureCategories': FeatureCategory.get_all_feature_cate(),
            'categories': Category.get_all_category(),
            'products': Product.get_all_product(),
            'banners': Banner.get_all_banner(),
            'range': range(len(Awesome.get_all_awesome()) // 8 + 1),
        }
        return render(request, 'homepage/index.html', context)


class ShopView(ListView):
    model = Product
    template_name = 'shop/shop.html'

    def get(self, request, slug=None):
        categories = Category.get_all_category()
        products = None
        quantity_product = len(Product.get_all_product())

        if slug:
            category = get_object_or_404(Category, slug=slug)
            products = Product.objects.filter(category=category)
        else:
            products = Product.get_all_product()

        context = {
            'categories': categories,
            'products': products,
            'quantity_product': quantity_product,
        }
        return render(request, self.template_name, context)


class DetailProduct(DetailView):
    model = Product
    template_name = 'detail/detail.html'


class CartView(ListView):
    model = CartItem
    template_name = 'cart/cart.html'


class LoginView(View):
    def get(self, request):
        return render(request, 'login/login.html')

# @login_required
# def add_to_cart(request, slug):
#     item = get_object_or_404(Product, slug=slug)
#     order_item, created = OrderItem.objects.get_or_create(
#         item=item,
#         user=request.user,
#         ordered=False
#     )
#     order_qs = Order.objects.filter(user=request.user, ordered=False)
#     if order_qs.exists():
#         order = order_qs[0]
#         # check if the order item is in the order
#         if order.items.filter(item__slug=item.slug).exists():
#             order_item.quantity += 1
#             order_item.save()
#             messages.info(request, "This item quantity was updated.")
#             return redirect("core:order-summary")
#         else:
#             order.items.add(order_item)
#             messages.info(request, "This item was added to your cart.")
#             return redirect("core:order-summary")
#     else:
#         ordered_date = timezone.now()
#         order = Order.objects.create(
#             user=request.user, ordered_date=ordered_date)
#         order.items.add(order_item)
#         messages.info(request, "This item was added to your cart.")
#         return redirect("core:order-summary")
