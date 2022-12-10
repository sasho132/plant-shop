from django.urls import path
from plant_shop.cart.views import update_item, checkout_view, cart_view

app_name = 'cart'

urlpatterns = [
        path('', cart_view, name='cart-summary'),
        path('update-item/', update_item, name='update-item'),
        path('checkout/', checkout_view, name='checkout'),
]
