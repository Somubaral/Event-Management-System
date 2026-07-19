import uuid

from django.db import transaction

from bookings.models import Booking
from tickets.models import (
    Ticket,
    TicketCategory
)

from .models import Payment

class PaymentService:

    @staticmethod
    @transaction.atomic
    def process_payment(
        booking_id,
        payment_result
    ):

        booking = Booking.objects.select_for_update().get(
            id=booking_id
        )

        if booking.status == "CONFIRMED":

            raise ValueError(
                "Payment already completed."
            )

        payment, created = Payment.objects.get_or_create(
            booking=booking,
            defaults={
                "amount": booking.total_amount,
                "transaction_id": str(uuid.uuid4())
            }
        )

        if payment.status == "SUCCESS":

            raise ValueError(
                "Duplicate payment request."
            )

        if payment_result == "SUCCESS":

            payment.status = "SUCCESS"

            booking.status = "CONFIRMED"

            payment.save()
            booking.save()

            ticket, _ = Ticket.objects.get_or_create(
                booking=booking
            )

            return {
                "payment": payment,
                "ticket": ticket
            }

        category = TicketCategory.objects.select_for_update().get(
            id=booking.ticket_category.id
        )

        # category.available_quantity += booking.quantity

        if booking.status != "FAILED":
            category.available_quantity += booking.quantity

            category.save()

        category.save()

        booking.status = "FAILED"

        payment.status = "FAILED"

        booking.save()
        payment.save()

        return {
            "payment": payment
        }