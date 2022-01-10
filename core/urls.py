from django.urls import path
from .views import LoginView, CheckoutView, SignUpView, log_out
from home.views import HomeView
from cart.views import CartView, add_to_cart, update_cart
from product.views import ShopView, DetailProduct
from order.views import PurchaseView, update_order


urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('product/<slug>/', DetailProduct.as_view(), name='product'),
    path('category/<slug>/', ShopView.as_view(), name='category'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<slug>', add_to_cart, name='add-to-cart'),
    path('check-out/', CheckoutView.as_view(), name='check-out'),
    path('account/sign-up/', SignUpView.as_view(), name='sign-up'),
    path('account/log-in/', LoginView.as_view(), name='log-in'),
    path('account/log-out/', log_out, name='log-out'),
    path('update-cart/', update_cart, name='update-cart'),
    path('update-order/', update_order, name='update-order'),
    path('purchase/', PurchaseView.as_view(), name='purchase'),
]
