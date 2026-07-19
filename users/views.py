from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import (
    RegisterSerializer,
    UserProfileSerializer
)

from .swagger import (
    register_schema,
    login_schema
)

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterAPIView(APIView):

    @register_schema
    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.save()

        return Response(
            {
                "success": True,
                "message": "User registered successfully",
                "data": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role
                }
            },
            status=status.HTTP_201_CREATED
        )

class LoginAPIView(APIView):

    @login_schema
    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:

            return Response(
                {
                    "success": False,
                    "message": "Username and password are required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(
            username=username,
            password=password
        )

        if not user:

            return Response(
                {
                    "success": False,
                    "message": "Invalid credentials."
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "success": True,
                "message": "Login successful",
                "data": {
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "role": user.role
                    },
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                }
            }
        )


class ProfileAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserProfileSerializer(
            request.user
        )

        return Response(
            {
                "success": True,
                "message": "Profile fetched successfully",
                "data": serializer.data
            }
        )