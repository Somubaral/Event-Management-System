from django.urls import path

from .views import (
    BookingCreateAPIView,
    MyBookingsAPIView,
    BookingDetailAPIView
)

urlpatterns = [

    path(
        "",
        BookingCreateAPIView.as_view(),
        name="booking-create"
    ),

    path(
        "my-bookings/",
        MyBookingsAPIView.as_view(),
        name="my-bookings"
    ),

    path(
        "<int:pk>/",
        BookingDetailAPIView.as_view(),
        name="booking-detail"
    ),
]