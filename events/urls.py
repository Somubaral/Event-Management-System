from django.urls import path

from .views import *

urlpatterns = [

    path(
        "",
        EventListCreateAPIView.as_view(),
        name="event-list-create"
    ),

    path(
        "my-events/",
        MyEventsAPIView.as_view(),
        name="my-events"
    ),

    path(
        "<int:pk>/",
        EventDetailAPIView.as_view(),
        name="event-detail"
    ),

    path(
        "<int:pk>/update/",
        EventUpdateAPIView.as_view(),
        name="event-update"
    ),

    path(
        "<int:pk>/cancel/",
        CancelEventAPIView.as_view(),
        name="event-cancel"
    ),

path(
    "<int:event_id>/bookings/",
    EventBookingsAPIView.as_view(),
    name="event-bookings"
),

path(
    "<int:event_id>/revenue/",
    EventRevenueAPIView.as_view(),
    name="event-revenue"
),
]