from django.urls import path

from .views import *

urlpatterns = [

    path(
        "event/<int:event_id>/",
        TicketCategoryCreateAPIView.as_view(),
        name="ticket-category-create"
    ),

    path(
        "event/<int:event_id>/list/",
        TicketCategoryListAPIView.as_view(),
        name="ticket-category-list"
    ),

    path(
        "<int:pk>/update/",
        TicketCategoryUpdateAPIView.as_view(),
        name="ticket-category-update"
    ),

    path(
        "my-tickets/",
        MyTicketsAPIView.as_view(),
        name="my-tickets"
    ),

    path(
        "details/<str:ticket_code>/",
        TicketDetailAPIView.as_view(),
        name="ticket-detail"
    ),

    path(
        "verify/<str:ticket_code>/",
        VerifyTicketAPIView.as_view(),
        name="verify-ticket"
    ),
]