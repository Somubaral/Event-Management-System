from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample
)


register_schema = extend_schema(
    tags=["Authentication"],
    summary="Register User",
    description="""
    Register a new user.

    Roles:
    - ORGANIZER
    - ATTENDEE
    """,
    examples=[
        OpenApiExample(
            "Organizer Example",
            value={
                "username": "organizer1",
                "email": "organizer@test.com",
                "password": "Password@123",
                "role": "ORGANIZER"
            }
        )
    ]
)

login_schema = extend_schema(
    tags=["Authentication"],
    summary="Login User",
    description="JWT Login API"
)