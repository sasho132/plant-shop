from django.urls import path
from plant_shop.orders.views import place_order, payments_view, order_complete_view

urlpatterns = [
    path('place-order/', place_order, name='place-order'),
    path('payments/', payments_view, name='payments'),
    path('order-complete/', order_complete_view, name='complete-order'),
]
