from django.db import models

from events.models import Event

import uuid


class TicketCategory(models.Model):

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="ticket_categories"
    )

    name = models.CharField(
        max_length=100
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total_quantity = models.PositiveIntegerField()

    available_quantity = models.PositiveIntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):

        if not self.pk:
            self.available_quantity = self.total_quantity

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.event.title} - {self.name}"

class Ticket(models.Model):

    booking = models.OneToOneField(
        "bookings.Booking",
        on_delete=models.CASCADE,
        related_name="ticket"
    )

    ticket_code = models.CharField(
        max_length=50,
        unique=True,
        blank=True
    )

    issued_at = models.DateTimeField(
        auto_now_add=True
    )

    is_valid = models.BooleanField(
        default=True
    )

    def save(self, *args, **kwargs):

        if not self.ticket_code:

            self.ticket_code = (
                f"TKT-{uuid.uuid4().hex[:10].upper()}"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.ticket_code