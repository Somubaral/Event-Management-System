from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticated
)
from rest_framework.response import Response

from users.permissions import (
    IsOrganizer
)

from .models import Venue
from .serializers import VenueSerializer
from .services import VenueService

from django.utils.dateparse import parse_datetime

from events.models import Event


class VenueListCreateAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        venues = Venue.objects.all()

        serializer = VenueSerializer(
            venues,
            many=True
        )

        return Response(
            {
                "success": True,
                "message": "Venues fetched successfully",
                "data": serializer.data
            }
        )

    def post(self, request):

        if request.user.role != "ORGANIZER":

            return Response(
                {
                    "success": False,
                    "message": "Only organizers can create venues"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = VenueSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        venue = VenueService.create_venue(
            serializer.validated_data
        )

        return Response(
            {
                "success": True,
                "message": "Venue created successfully",
                "data": VenueSerializer(
                    venue
                ).data
            },
            status=status.HTTP_201_CREATED
        )

class VenueDetailAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request, pk):

        try:
            venue = Venue.objects.get(
                pk=pk
            )

        except Venue.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Venue not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = VenueSerializer(
            venue
        )

        return Response(
            {
                "success": True,
                "message": "Venue fetched successfully",
                "data": serializer.data
            }
        )

class VenueAvailabilityAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        venue_id = request.GET.get("venue")

        start = request.GET.get("start")

        end = request.GET.get("end")

        if not venue_id or not start or not end:

            return Response(
                {
                    "success": False,
                    "message": (
                        "venue, start and end are required"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        start_time = parse_datetime(start)

        end_time = parse_datetime(end)

        conflict = Event.objects.filter(
            venue_id=venue_id,
            status="ACTIVE",
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exists()

        return Response(
            {
                "success": True,
                "available": not conflict
            }
        )