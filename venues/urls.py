from django.urls import path

from .views import *

urlpatterns = [

    path(
        "",
        VenueListCreateAPIView.as_view(),
        name="venue-list-create"
    ),

    path(
        "<int:pk>/",
        VenueDetailAPIView.as_view(),
        name="venue-detail"
    ),

path(
    "availability/",
    VenueAvailabilityAPIView.as_view(),
    name="venue-availability"
),

]