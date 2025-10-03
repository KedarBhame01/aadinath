# Add these URL patterns to your students/urls.py

from django.contrib import admin
from django.urls import path, include
from . import views
from .views import Cart_API

urlpatterns = [
    # API endpoints (existing)
    path('add/', Cart_API.as_view({'post':'create'})),
    path('all/', Cart_API.as_view({'get':'list'})),
    path('details/<int:pk>/', Cart_API.as_view({'get':'retrieve'})),
    path('partialupdate/<int:pk>/', Cart_API.as_view({'patch': 'partial_update'})),
    path('update/<int:pk>/', Cart_API.as_view({'put':'update'})),
    path('delete/<int:pk>/', Cart_API.as_view({'delete':'destroy'})),
    # path('login/', UserLoginAPI.as_view({'post':'login'})),
    # path('search/', Cart_API.as_view({'post':'search'})),
    path('user/<int:user>/', Cart_API.as_view({'get':'cart_user_list'}), name='cart_user_list'),
    
    
]