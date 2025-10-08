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

from decouple import config

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

    


class Cart_API(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = User_serializer 
    
    def cart_user_list(self, request,user, *args, **kwargs):
        try:
            queryset = self.get_queryset().filter(user_id=user)
            if not queryset.exists():
                return error_response(f"No cart records found for user id {user}", code=status.HTTP_404_NOT_FOUND)
            serializer = self.get_serializer(queryset, many=True)
            return success_response("Filtered cart records", serializer.data, code=status.HTTP_200_OK)
        except Exception as e:
            return error_response(f"Error fetching filtered cart records: {e}", code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # ✅ List
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return success_response("All records fetched", serializer.data)
        except Exception as e:
            return error_response(f"Error fetching list: {e}", code=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # ✅ Retrieve
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return success_response("Cart record fetched", serializer.data)
        except Cart.DoesNotExist:
            return error_response("Cart record not found", code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return error_response(f"Error fetching record: {e}", code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ✅ Create
    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        product_id = request.data.get('product')
        try:
            cart_item = Cart.objects.filter(user_id=user_id, product_id=product_id).first()
            if cart_item:
                cart_item.quantity = cart_item.quantity + 1
                cart_item.save()
                return Response({
                    "message": "Existing cart item, quantity increased",
                    "cart_item": self.get_serializer(cart_item).data
                }, status=status.HTTP_200_OK)
            else:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({
                    "message": "New cart item created",
                    "cart_item": serializer.data
                }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                "message": f"Error: {e}"
            }, status=status.HTTP_400_BAD_REQUEST)
    # ✅ Update
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            new_user_id = request.data.get('user', instance.user)
            new_product_id = request.data.get('product', instance.product)
            # Prevent duplicate (user, product)
            existing = Cart.objects.filter(user_id=new_user_id, product_id=new_product_id).exclude(pk=instance.pk).first()
            if existing:
                # Optional: combine quantities instead, or raise error
                existing.quantity = request.data.get('quantity', 1)
                existing.save()
                instance.delete()  # Remove old record to keep unique
                return success_response("Combined with existing cart item", self.get_serializer(existing).data)
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return success_response("Record updated successfully", serializer.data)
        except Exception as e:
            return error_response(f"Error updating record: {e}")

    # ✅ Partial Update
    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            new_user_id = request.data.get('user', instance.user)
            new_product_id = request.data.get('product', instance.product)
            existing = Cart.objects.filter(user_id=new_user_id, product_id=new_product_id).exclude(pk=instance.pk).first()
            if existing:
                existing.quantity = request.data.get('quantity', 1)
                existing.save()
                instance.delete()
                return success_response("Combined with existing cart item (partial)", self.get_serializer(existing).data)
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return success_response("Record partially updated successfully", serializer.data)
        except Exception as e:
            return error_response(f"Error in partial update: {e}")

    # ✅ Destroy
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return success_response("Record deleted successfully")
        except Exception as e:
            return error_response(f"Error deleting record: {e}")



# Razorpay Configuration
RAZORPAY_API_KEY = config('RAZORPAY_API_KEY', default='your_test_key_id')
RAZORPAY_API_SECRET = config('RAZORPAY_API_SECRET', default='your_test_key_secret')

# Or directly (not recommended for production)
# RAZORPAY_API_KEY = 'rzp_test_your_key_id'
# RAZORPAY_API_SECRET = 'your_key_secret'  