from rest_framework import serializers
from .models import PaymentOrder

class PaymentOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentOrder
        fields = ['id', 'user', 'amount', 'currency', 'razorpay_order_id', 
                 'razorpay_payment_id', 'status', 'purpose', 'created_at']
        read_only_fields = ['id', 'razorpay_order_id', 'razorpay_payment_id', 'created_at']

class CreateOrderSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    purpose = serializers.CharField(max_length=500, required=False)

class VerifyPaymentSerializer(serializers.Serializer):
    razorpay_order_id = serializers.CharField()
    razorpay_payment_id = serializers.CharField()
    razorpay_signature = serializers.CharField()
