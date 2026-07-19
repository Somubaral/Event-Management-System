from rest_framework import serializers

from .models import (
    TicketCategory,
    Ticket
)


class TicketCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = TicketCategory

        fields = "__all__"

        read_only_fields = (
            "available_quantity",
            "event",
        )


class TicketSerializer(serializers.ModelSerializer):

    booking_id = serializers.IntegerField(
        source="booking.id",
        read_only=True
    )

    event_name = serializers.CharField(
        source="booking.event.title",
        read_only=True
    )

    user = serializers.CharField(
        source="booking.user.username",
        read_only=True
    )

    class Meta:

        model = Ticket

        fields = "__all__"