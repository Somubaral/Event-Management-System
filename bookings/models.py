from django.db import models
from django.conf import settings

from events.models import Event
from tickets.models import TicketCategory


class Booking(models.Model):

    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("FAILED", "Failed"),
        ("CANCELLED", "Cancelled"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    ticket_category = models.ForeignKey(
        TicketCategory,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    quantity = models.PositiveIntegerField()

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Booking #{self.id}"