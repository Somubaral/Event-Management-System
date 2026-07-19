from decimal import Decimal

from django.db import transaction

from tickets.models import TicketCategory

from .models import Booking

from django.utils import timezone


class BookingService:



    @staticmethod
    @transaction.atomic
    def create_booking(
        user,
        category_id,
        quantity
    ):

        if user.role != "ATTENDEE":
            raise ValueError(
                "Only attendees can book tickets."
            )

        category = TicketCategory.objects.select_for_update().get(
            id=category_id
        )

        if category.event.status != "ACTIVE":
            raise ValueError(
                "This event is not available for booking."
            )

        if category.event.start_time <= timezone.now():
            raise ValueError(
                "Booking closed for this event."
            )

        if quantity <= 0:
            raise ValueError(
                "Quantity must be greater than zero."
            )

        if category.available_quantity < quantity:
            raise ValueError(
                "Not enough tickets available."
            )

        category.available_quantity -= quantity

        category.save()

        total_amount = (
            Decimal(category.price) * quantity
        )

        booking = Booking.objects.create(
            user=user,
            event=category.event,
            ticket_category=category,
            quantity=quantity,
            total_amount=total_amount,
            status="PENDING"
        )

        return booking