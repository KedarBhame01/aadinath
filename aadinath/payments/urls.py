from django.urls import path
from .views import (
    CreateOrderView,
    VerifyPaymentView, 
    PaymentHistoryView,
    PaymentStatusView,
    payment_page  # Add this import
)

urlpatterns = [
    path('', payment_page, name='payment-page'),  # Payment page
    path('create-order/', CreateOrderView.as_view(), name='create-order'),
    path('verify-payment/', VerifyPaymentView.as_view(), name='verify-payment'),
    path('history/', PaymentHistoryView.as_view(), name='payment-history'),
    path('status/<str:order_id>/', PaymentStatusView.as_view(), name='payment-status'),
    # Add success and failure pages
    # path('success/', payment_success, name='payment-success'),
    # path('failed/', payment_failed, name='payment-failed'),
]
