# Add these URL patterns to your students/urls.py

from django.contrib import admin
from django.urls import path, include
from . import views
from .views import Admin_API, AdminLoginAPI

urlpatterns = [
    # API endpoints (existing)
    path('add/', Admin_API.as_view({'post':'create'})),
    path('all/', Admin_API.as_view({'get':'list'})),
    path('details/<int:pk>/', Admin_API.as_view({'get':'retrieve'})),
    path('partialupdate/<int:pk>/', Admin_API.as_view({'patch': 'partial_update'})),
    path('update/<int:pk>/', Admin_API.as_view({'put':'update'})),
    path('delete/<int:pk>/', Admin_API.as_view({'delete':'destroy'})),
    path('login/', AdminLoginAPI.as_view({'post':'login'})),
    path('search/', Admin_API.as_view({'post':'search'})),
    
    
]