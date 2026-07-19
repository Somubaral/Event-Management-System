from django.urls import path

from .views import (
    PaymentProcessAPIView,
    PaymentRetryAPIView
)

urlpatterns = [

    path(
        "process/",
        PaymentProcessAPIView.as_view(),
        name="payment-process"
    ),

    path(
        "retry/",
        PaymentRetryAPIView.as_view(),
        name="payment-retry"
    ),
]