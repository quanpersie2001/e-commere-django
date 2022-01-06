from django.urls import path
from .views import HomeView, ShopView, DetailProduct, CartView, LoginView
urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('index/', HomeView.as_view(), name='index'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('product/<slug>/', DetailProduct.as_view(), name='product'),
    path('category/<slug>/', ShopView.as_view(), name='category'),
    path('cart/', CartView.as_view(), name='cart'),
    path('login/', LoginView.as_view(), name='login'),
]
