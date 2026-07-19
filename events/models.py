from django.db import models
from django.conf import settings

from venues.models import Venue


class Event(models.Model):

    STATUS_CHOICES = (
        ("ACTIVE", "Active"),
        ("CANCELLED", "Cancelled"),
    )

    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="events"
    )

    venue = models.ForeignKey(
        Venue,
        on_delete=models.CASCADE,
        related_name="events"
    )

    title = models.CharField(
        max_length=255
    )

    description = models.TextField()

    start_time = models.DateTimeField()

    end_time = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ACTIVE"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title
