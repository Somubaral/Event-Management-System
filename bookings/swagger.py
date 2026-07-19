from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample
)

create_booking_schema = extend_schema(
    tags=["Bookings"],
    summary="Create Booking",
    description="""
    Creates a booking and reserves tickets.

    Prevents:
    - Overselling
    - Negative inventory
    """,
    examples=[
        OpenApiExample(
            "Booking Example",
            value={
                "ticket_category": 1,
                "quantity": 2
            }
        )
    ]
)