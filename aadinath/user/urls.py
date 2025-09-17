# Add these URL patterns to your students/urls.py

from django.contrib import admin
from django.urls import path, include
from . import views
from .views import User_API, UserLoginAPI

urlpatterns = [
    # API endpoints (existing)
    path('add/', User_API.as_view({'post':'create'})),
    path('all/', User_API.as_view({'get':'list'})),
    path('details/<int:pk>/', User_API.as_view({'get':'retrieve'})),
    path('partialupdate/<int:pk>/', User_API.as_view({'patch': 'partial_update'})),
    path('update/<int:pk>/', User_API.as_view({'put':'update'})),
    path('delete/<int:pk>/', User_API.as_view({'delete':'destroy'})),
    path('login/', UserLoginAPI.as_view({'post':'login'})),
    path('search/', User_API.as_view({'post':'search'})),
    
    
]