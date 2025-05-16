# recommendations/urls.py
from django.urls import path
from .views import (
    recommend_products,
    recommendation_dashboard,
    recommend_product_page  # ⬅️ añade esta línea
)

urlpatterns = [
    path("recommend/<int:user_id>/", recommend_products, name="recommend_products"),
    path("dashboard/", recommendation_dashboard, name="recommendation_dashboard"),
    path('product/<str:asin>/', recommend_product_page, name='recommend_product'),
]
