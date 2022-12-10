from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('plant_shop.store.urls')),
    path('accounts/', include('plant_shop.accounts.urls')),
    path('categories/', include('plant_shop.category.urls')),
    path('cart/', include('plant_shop.cart.urls')),
    path('orders/', include('plant_shop.orders.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
"""
