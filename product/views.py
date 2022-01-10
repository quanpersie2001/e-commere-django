from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from cart.models import Cart
from product.models import Product, Category


# Create your views here.


class ShopView(ListView):
    model = Product
    template_name = 'shop/shop.html'

    def get(self, request, slug=None):
        categories = Category.get_all_category()
        products = None
        quantity_product = len(Product.get_all_product())
        cart_quantity = Cart.item_quantity(request.user)

        order_price_dis = 'Ascending'
        order_name_dis = 'Descending'
        search_txt = ''

        if slug:
            category = get_object_or_404(Category, slug=slug)
            products = Product.get_product_by_category(category)
        else:
            products = Product.get_all_product().order_by('price', 'title')

        if 'search' in request.GET:
            search = request.GET['search']
            products = products.filter(title__icontains=search)
            search_txt = search

        if 'sortByPrice' in request.GET:
            order_by = request.GET['sortByPrice']
            if order_by == 'asc':
                products = products.order_by('price')
                order_price_dis = 'Ascending'
            elif order_by == 'desc':
                products = products.order_by('-price')
                order_price_dis = 'Descending'

        if 'sortByName' in request.GET:
            order_by = request.GET['sortByName']
            if order_by == 'asc':
                products = products.order_by('title')
                order_name_dis = 'Ascending'
            elif order_by == 'desc':
                products = products.order_by('-title')
                order_name_dis = 'Descending'

        context = {
            'categories': categories,
            'products': products,
            'quantity_product': quantity_product,
            'order_price': order_price_dis,
            'order_name': order_name_dis,
            'search_txt': search_txt,
            'cart_quantity': cart_quantity,
        }
        return render(request, self.template_name, context)


class DetailProduct(DetailView):
    model = Product
    template_name = 'detail/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_quantity'] = Cart.item_quantity(self.request.user)
        return context
