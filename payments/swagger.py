from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample
)

payment_schema = extend_schema(
    tags=["Payments"],
    summary="Process Payment",
    description="""
    Dummy Payment API

    Supports:

    SUCCESS
    FAILED
    """,
    examples=[
        OpenApiExample(
            "Success Example",
            value={
                "booking_id": 1,
                "payment_result": "SUCCESS"
            }
        ),
        OpenApiExample(
            "Failure Example",
            value={
                "booking_id": 1,
                "payment_result": "FAILED"
            }
        )
    ]
)

retry_schema = extend_schema(
    tags=["Payments"],
    summary="Retry Failed Payment"
)