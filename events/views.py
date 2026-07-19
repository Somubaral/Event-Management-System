from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Event
from .serializers import EventSerializer
from .services import EventService

from .swagger import (
    create_event_schema,
    list_event_schema
)
from tickets.models import Ticket

from bookings.models import Booking
from bookings.serializers import BookingSerializer
from django.db.models import Sum


class EventListCreateAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    @list_event_schema
    def get(self, request):

        events = Event.objects.filter(
            status="ACTIVE"
        )

        serializer = EventSerializer(
            events,
            many=True
        )

        return Response(
            {
                "success": True,
                "message": "Events fetched successfully",
                "data": serializer.data
            }
        )

    @create_event_schema
    def post(self, request):

        if request.user.role != "ORGANIZER":

            return Response(
                {
                    "success": False,
                    "message": "Only organizers can create events."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = EventSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:

            EventService.validate_future_date(
                serializer.validated_data["start_time"]
            )

            EventService.validate_time_range(
                serializer.validated_data["start_time"],
                serializer.validated_data["end_time"]
            )

            EventService.validate_venue_conflict(
                serializer.validated_data["venue"],
                serializer.validated_data["start_time"],
                serializer.validated_data["end_time"]
            )

        except ValueError as e:

            return Response(
                {
                    "success": False,
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        event = serializer.save(
            organizer=request.user
        )

        return Response(
            {
                "success": True,
                "message": "Event created successfully",
                "data": EventSerializer(
                    event
                ).data
            },
            status=status.HTTP_201_CREATED
        )

class EventDetailAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    @list_event_schema
    def get(self, request, pk):

        try:
            event = Event.objects.get(
                pk=pk
            )

        except Event.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Event not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = EventSerializer(
            event
        )

        return Response(
            {
                "success": True,
                "data": serializer.data
            }
        )

class EventUpdateAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def put(self, request, pk):

        try:
            event = Event.objects.get(pk=pk)

        except Event.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Event not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if event.organizer != request.user:
            return Response(
                {
                    "success": False,
                    "message": "You cannot edit another organizer's event."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = EventSerializer(
            event,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)

        start_time = serializer.validated_data.get(
            "start_time",
            event.start_time
        )

        end_time = serializer.validated_data.get(
            "end_time",
            event.end_time
        )

        venue = serializer.validated_data.get(
            "venue",
            event.venue
        )

        try:

            EventService.validate_future_date(
                start_time
            )

            EventService.validate_time_range(
                start_time,
                end_time
            )

            conflict = Event.objects.filter(
                venue=venue,
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exclude(
                id=event.id
            ).exists()

            if conflict:
                raise ValueError(
                    "Venue already booked during this time."
                )

        except ValueError as e:

            return Response(
                {
                    "success": False,
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()

        return Response(
            {
                "success": True,
                "message": "Event updated successfully",
                "data": serializer.data
            }
        )

class CancelEventAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def patch(self, request, pk):

        try:
            event = Event.objects.get(
                pk=pk
            )

        except Event.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Event not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if event.organizer != request.user:

            return Response(
                {
                    "success": False,
                    "message": "Unauthorized"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        event.status = "CANCELLED"

        event.save()



        Ticket.objects.filter(
            booking__event=event
        ).update(
            is_valid=False
        )

        return Response(
            {
                "success": True,
                "message": "Event cancelled successfully"
            }
        )

class MyEventsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        events = Event.objects.filter(
            organizer=request.user
        )

        serializer = EventSerializer(
            events,
            many=True
        )

        return Response(
            {
                "success": True,
                "data": serializer.data
            }
        )

class EventBookingsAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request, event_id):

        try:
            event = Event.objects.get(
                id=event_id
            )

        except Event.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Event not found"
                },
                status=404
            )

        if event.organizer != request.user:

            return Response(
                {
                    "success": False,
                    "message": "Unauthorized"
                },
                status=403
            )

        bookings = Booking.objects.filter(
            event=event
        )

        serializer = BookingSerializer(
            bookings,
            many=True
        )

        return Response(
            {
                "success": True,
                "data": serializer.data
            }
        )

class EventRevenueAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):

        try:

            event = Event.objects.get(
                id=event_id
            )

        except Event.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Event not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if event.organizer != request.user:

            return Response(
                {
                    "success": False,
                    "message": "Unauthorized"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        confirmed_bookings = Booking.objects.filter(
            event=event,
            status="CONFIRMED"
        )

        revenue = confirmed_bookings.aggregate(
            total=Sum("total_amount")
        )["total"] or 0

        return Response(
            {
                "success": True,
                "event": event.title,
                "confirmed_bookings": confirmed_bookings.count(),
                "revenue": revenue
            }
        )