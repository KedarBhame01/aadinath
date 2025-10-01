from django.shortcuts import render
from django.db.models import Q
from .serializers import User_serializer
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status,filters
# from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Cart
# for show swagger parameter
from drf_yasg.utils import swagger_auto_schema
# JWT authentication class
#for jwt json web token
import jwt
from datetime import timedelta
from django.utils import timezone
from django.conf import settings

from utils.base_viewsets import BaseCRUDViewSet
from utils.base_viewsets import success_response, error_response
import logging

logger = logging.getLogger(__name__)
# Create your views here.

    


class Cart_API(BaseCRUDViewSet):
    queryset = Cart.objects.all()
    serializer_class = User_serializer 
    
    # @swagger_auto_schema(
    #     methods=['post'],
    #     request_body=User_search_serializer,
    #     responses={200: User_login_serializer(many=True)}
    # )
    # @action(detail=False, methods=['post'], url_path='search')
    # def search(self, request, *args, **kwargs):
    #         try:
    #             search_term = request.data.get('search_term')
    #             if not search_term:
    #                     return Response({"message": "Please provide a search term"},
    #                                     status=status.HTTP_400_BAD_REQUEST)
    #             search_in = request.data.get('search_in').lower()
                
               
    #             search_results = User.objects.none()
    #             if search_in == 'email':
    #                     search_results = User.objects.filter(email=search_term)
                
    #             if not search_results.exists():
    #                 return error_response(
    #                 f"No user found matching '{search_term}' in {search_in}"
    #                 )
    #             serializer = User_serializer(search_results, many=True)

    #             return success_response("Search results", serializer.data)
    #         except Exception as e:
    #             return error_response(f"Error searching admin: {e}")   
    
    # def create(self, request, *args, **kwargs):
    #     try:
    #         data = request.data
    #         if not data:
    #             return error_response('No data provided.', code=status.HTTP_400_BAD_REQUEST)

    #         # Check required fields
    #         for field in ['email', 'password']:
    #             if not data.get(field):
    #                 return error_response(f'Missing field: {field}', code=status.HTTP_400_BAD_REQUEST)

    #         # Check if username exists
    #         if User.objects.filter(email=data['email']).exists():
    #             return error_response('user already exists.', code=status.HTTP_409_CONFLICT)

    #         # Hash password
    #         data = data.copy()
    #         data['password'] = make_password(data['password'])

    #         serializer = self.get_serializer(data=data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()

    #         return success_response(
    #             "user registered successfully",
    #                                 serializer.data,
    #                                 code=status.HTTP_201_CREATED
    #         )
    #     except Exception as e:
    #         logger.error(f"Error creating user: {e}")
    #         return error_response('Registration failed. Please try again later.', code=status.HTTP_500_INTERNAL_SERVER_ERROR)
            