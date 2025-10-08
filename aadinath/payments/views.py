import razorpay
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import PaymentOrder
from .serializers import (
    PaymentOrderSerializer, 
    CreateOrderSerializer, 
    VerifyPaymentSerializer
)

# Initialize Razorpay Client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'Invalid data',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        amount = serializer.validated_data['amount']
        purpose = serializer.validated_data.get('purpose', '')
        
        # Convert amount to paise (Razorpay uses smallest currency unit)
        amount_in_paise = int(amount * 100)
        
        # Create Razorpay order
        try:
            razorpay_order = razorpay_client.order.create({
                'amount': amount_in_paise,
                'currency': 'INR',
                'receipt': f'order_{request.user.id}_{int(amount)}',
                'payment_capture': 1  # Auto capture payment
            })
        except Exception as e:
            return Response({
                'status': 'error',
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Failed to create Razorpay order',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Save order in database
        payment_order = PaymentOrder.objects.create(
            user=request.user,
            amount=amount,
            razorpay_order_id=razorpay_order['id'],
            purpose=purpose,
            status='PENDING'
        )
        
        return Response({
            'status': 'success',
            'code': status.HTTP_201_CREATED,
            'message': 'Order created successfully',
            'data': {
                'order_id': razorpay_order['id'],
                'amount': amount_in_paise,
                'currency': 'INR',
                'key': settings.RAZORPAY_API_KEY,  # Frontend needs this
                'payment_order_id': payment_order.id
            }
        }, status=status.HTTP_201_CREATED)

class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = VerifyPaymentSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'Invalid data',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        order_id = serializer.validated_data['razorpay_order_id']
        payment_id = serializer.validated_data['razorpay_payment_id']
        signature = serializer.validated_data['razorpay_signature']
        
        # Get payment order
        payment_order = get_object_or_404(
            PaymentOrder, 
            razorpay_order_id=order_id,
            user=request.user
        )
        
        # Verify payment signature
        try:
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            
            # This will raise an exception if signature is invalid
            razorpay_client.utility.verify_payment_signature(params_dict)
            
            # Update payment order
            payment_order.razorpay_payment_id = payment_id
            payment_order.razorpay_signature = signature
            payment_order.status = 'COMPLETED'
            payment_order.save()
            
            return Response({
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Payment verified successfully',
                'data': PaymentOrderSerializer(payment_order).data
            }, status=status.HTTP_200_OK)
            
        except razorpay.errors.SignatureVerificationError:
            payment_order.status = 'FAILED'
            payment_order.save()
            
            return Response({
                'status': 'error',
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'Payment verification failed'
            }, status=status.HTTP_400_BAD_REQUEST)

class PaymentHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        payments = PaymentOrder.objects.filter(user=request.user)
        serializer = PaymentOrderSerializer(payments, many=True)
        
        return Response({
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Payment history retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

class PaymentStatusView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, order_id):
        payment_order = get_object_or_404(
            PaymentOrder, 
            razorpay_order_id=order_id,
            user=request.user
        )
        
        return Response({
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Payment status retrieved',
            'data': PaymentOrderSerializer(payment_order).data
        }, status=status.HTTP_200_OK)
