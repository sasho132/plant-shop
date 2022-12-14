from django.urls import path
from plant_shop.store.views import IndexView, ProductDetailsView, products_view, ContactUsView

urlpatterns = [
    path('', IndexView.as_view(), name='home-page'),
    path('store/', products_view, name='store'),
    path('store/<slug:slug>/', products_view, name='products-by-category'),
    path('store/details/<slug:category_slug>/<slug:slug>/',
         ProductDetailsView.as_view(), name='product-details'),
    path('contact/', ContactUsView.as_view(), name='contact'),
]
