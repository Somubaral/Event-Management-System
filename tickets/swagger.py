from drf_spectacular.utils import (
    extend_schema
)

my_tickets_schema = extend_schema(
    tags=["Tickets"],
    summary="My Tickets"
)

verify_ticket_schema = extend_schema(
    tags=["Tickets"],
    summary="Verify Ticket",
    description="""
    Organizer verifies ticket validity.
    """
)