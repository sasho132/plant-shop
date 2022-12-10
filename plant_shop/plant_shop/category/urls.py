from django.urls import path
from plant_shop.category.views import CategoriesView

urlpatterns = [
    path('', CategoriesView.as_view(), name='categories'),
]
