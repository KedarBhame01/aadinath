from django.urls import path
from .views import (
    CreateOrderView,
    VerifyPaymentView, 
    PaymentHistoryView,
    PaymentStatusView
)

urlpatterns = [
    path('create-order/', CreateOrderView.as_view(), name='create-order'),
    path('verify-payment/', VerifyPaymentView.as_view(), name='verify-payment'),
    path('history/', PaymentHistoryView.as_view(), name='payment-history'),
    path('status/<str:order_id>/', PaymentStatusView.as_view(), name='payment-status'),
]
