from drf_spectacular.utils import (
    extend_schema
)

create_venue_schema = extend_schema(
    tags=["Venues"],
    summary="Create Venue"
)

list_venue_schema = extend_schema(
    tags=["Venues"],
    summary="List Venues"
)