from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from events.models import Event

from .models import (
    Ticket,
    TicketCategory
)
from .serializers import (
    TicketSerializer,
    TicketCategorySerializer
)

class TicketCategoryCreateAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request, event_id):

        try:
            event = Event.objects.get(
                pk=event_id
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
                    "message": "Only owner organizer can manage tickets."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = TicketCategorySerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        ticket_category = serializer.save(
            event=event
        )

        return Response(
            {
                "success": True,
                "message": "Ticket category created successfully",
                "data": TicketCategorySerializer(
                    ticket_category
                ).data
            },
            status=status.HTTP_201_CREATED
        )

class TicketCategoryListAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request, event_id):

        categories = TicketCategory.objects.filter(
            event_id=event_id
        )

        serializer = TicketCategorySerializer(
            categories,
            many=True
        )

        return Response(
            {
                "success": True,
                "data": serializer.data
            }
        )

class TicketCategoryUpdateAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def put(self, request, pk):

        try:
            category = TicketCategory.objects.get(
                pk=pk
            )

        except TicketCategory.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Ticket category not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if category.event.organizer != request.user:

            return Response(
                {
                    "success": False,
                    "message": "Unauthorized"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = TicketCategorySerializer(
            category,
            data=request.data,
            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        new_total = request.data.get(
            "total_quantity"
        )

        if new_total:

            new_total = int(new_total)

            sold = (
                    category.total_quantity
                    - category.available_quantity
            )

            if new_total < sold:
                return Response(
                    {
                        "success": False,
                        "message": (
                            "Cannot reduce below already sold tickets."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer.save()

        return Response(
            {
                "success": True,
                "message": "Ticket category updated",
                "data": serializer.data
            }
        )

class MyTicketsAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        tickets = Ticket.objects.filter(
            booking__user=request.user
        )

        serializer = TicketSerializer(
            tickets,
            many=True
        )

        return Response(
            {
                "success": True,
                "data": serializer.data
            }
        )

class TicketDetailAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request,
        ticket_code
    ):

        try:

            ticket = Ticket.objects.get(
                ticket_code=ticket_code
            )

        except Ticket.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Ticket not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if ticket.booking.user != request.user:

            return Response(
                {
                    "success": False,
                    "message": "Access denied."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = TicketSerializer(
            ticket
        )

        return Response(
            {
                "success": True,
                "data": serializer.data
            }
        )

class VerifyTicketAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request,
        ticket_code
    ):

        try:

            ticket = Ticket.objects.get(
                ticket_code=ticket_code
            )

        except Ticket.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Invalid ticket."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        event = ticket.booking.event

        if event.organizer != request.user:

            return Response(
                {
                    "success": False,
                    "message": "Only organizer can verify tickets."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = TicketSerializer(
            ticket
        )

        return Response(
            {
                "success": True,
                "message": "Valid ticket",
                "data": serializer.data
            }
        )