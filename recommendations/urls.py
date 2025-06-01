# recommendations/urls.py
from django.urls import path
from .views import (
    evaluation_dashboard,
    recommend_products,
    recommend_product_page  # ⬅️ añade esta línea
)

urlpatterns = [
    path("recommend/<int:user_id>/", recommend_products, name="recommend_products"),
    path('dashboard/', evaluation_dashboard, name='evaluation_dashboard'),
    path('product/<str:asin>/', recommend_product_page, name='recommend_product'),
]
