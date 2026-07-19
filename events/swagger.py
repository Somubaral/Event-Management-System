from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample
)

create_event_schema = extend_schema(
    tags=["Events"],
    summary="Create Event",
    description="""
    Create an event.

    Rules:

    - Future date only
    - Venue must not overlap
    - Only organizers allowed
    """,
    examples=[
        OpenApiExample(
            "Event Example",
            value={
                "venue": 1,
                "title": "Rock Concert",
                "description": "Live Music",
                "start_time": "2026-08-20T10:00:00Z",
                "end_time": "2026-08-20T14:00:00Z"
            }
        )
    ]
)

list_event_schema = extend_schema(
    tags=["Events"],
    summary="List Events"
)