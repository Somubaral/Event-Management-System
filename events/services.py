from django.utils import timezone

from .models import Event


class EventService:

    @staticmethod
    def validate_future_date(start_time):

        if start_time <= timezone.now():
            raise ValueError(
                "Event cannot be created for a past date."
            )

    @staticmethod
    def validate_time_range(
        start_time,
        end_time
    ):

        if end_time <= start_time:
            raise ValueError(
                "End time must be after start time."
            )

    @staticmethod
    def validate_venue_conflict(
        venue,
        start_time,
        end_time,
        event_id=None
    ):

        queryset = Event.objects.filter(
            venue=venue,
            status="ACTIVE",
            start_time__lt=end_time,
            end_time__gt=start_time
        )

        if event_id:
            queryset = queryset.exclude(
                id=event_id
            )

        if queryset.exists():

            raise ValueError(
                "Venue already booked during this time slot."
            )