from django.urls import include, path
from . import views  

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('', views.home, name='home'),  
]
