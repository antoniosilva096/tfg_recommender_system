from django.urls import include, path
from . import views  

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('recommendations/', include('recommendations.urls')),
    path('', views.home, name='home'),  
]
