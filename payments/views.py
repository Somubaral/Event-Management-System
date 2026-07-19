from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from bookings.models import Booking

from .services import PaymentService

from .swagger import (
    payment_schema,
    retry_schema
)


class PaymentProcessAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    @payment_schema
    def post(self, request):

        booking_id = request.data.get(
            "booking_id"
        )

        payment_result = request.data.get(
            "payment_result"
        )

        try:

            booking = Booking.objects.get(
                id=booking_id
            )

            if booking.user != request.user:

                return Response(
                    {
                        "success": False,
                        "message": "Access denied."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            if booking.status == "CONFIRMED":

                return Response(
                    {
                        "success": True,
                        "message": "Payment already completed."
                    },
                    status=status.HTTP_200_OK
                )

            result = PaymentService.process_payment(
                booking_id,
                payment_result
            )

            response_data = {
                "success": True,
                "message": "Payment processed successfully"
            }

            if (
                payment_result == "SUCCESS"
                and "ticket" in result
            ):
                response_data["ticket_code"] = (
                    result["ticket"].ticket_code
                )

            return Response(
                response_data,
                status=status.HTTP_200_OK
            )

        except Booking.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Booking not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class PaymentRetryAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    @retry_schema
    def post(self, request):

        booking_id = request.data.get(
            "booking_id"
        )

        try:

            booking = Booking.objects.get(
                id=booking_id
            )

            if booking.user != request.user:

                return Response(
                    {
                        "success": False,
                        "message": "Access denied."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            if booking.status != "FAILED":

                return Response(
                    {
                        "success": False,
                        "message": "Only failed bookings can retry."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            booking.status = "PENDING"

            booking.save()

            return Response(
                {
                    "success": True,
                    "message": "Retry initiated."
                }
            )

        except Booking.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Booking not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )