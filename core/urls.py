from django.urls import path
from .views import HomeView, ShopView, DetailProduct
urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('index/', HomeView.as_view(), name='index'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('product/<slug>/', DetailProduct.as_view(), name='product')
]
