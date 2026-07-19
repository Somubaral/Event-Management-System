from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Booking
from .serializers import BookingSerializer
from .services import BookingService

from .swagger import (
    create_booking_schema
)


class BookingCreateAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    @create_booking_schema
    def post(self, request):

        category_id = request.data.get(
            "ticket_category"
        )

        quantity = int(
            request.data.get("quantity", 1)
        )

        try:

            booking = BookingService.create_booking(
                request.user,
                category_id,
                quantity
            )

            return Response(
                {
                    "success": True,
                    "message": "Booking created successfully",
                    "data": {
                        "booking_id": booking.id,
                        "amount": booking.total_amount,
                        "status": booking.status
                    }
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

class MyBookingsAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        bookings = Booking.objects.filter(
            user=request.user
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

class BookingDetailAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request, pk):

        try:

            booking = Booking.objects.get(
                pk=pk
            )

        except Booking.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Booking not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if booking.user != request.user:

            return Response(
                {
                    "success": False,
                    "message": "Access denied."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = BookingSerializer(
            booking
        )

        return Response(
            {
                "success": True,
                "data": serializer.data
            }
        )