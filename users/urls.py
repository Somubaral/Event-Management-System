# from django.urls import path
#
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView
# )
#
# from .views import (
#     RegisterAPIView,
#     ProfileAPIView
# )
#
# urlpatterns = [
#
#     path(
#         "register/",
#         RegisterAPIView.as_view(),
#         name="register"
#     ),
#
#     path(
#         "login/",
#         TokenObtainPairView.as_view(),
#         name="login"
#     ),
#
#     path(
#         "refresh/",
#         TokenRefreshView.as_view(),
#         name="refresh"
#     ),
#
#     path(
#         "me/",
#         ProfileAPIView.as_view(),
#         name="profile"
#     ),
# ]


from django.urls import path

from .views import (
    RegisterAPIView,
    LoginAPIView,
    ProfileAPIView
)

urlpatterns = [

    path(
        "register/",
        RegisterAPIView.as_view(),
        name="register"
    ),

    path(
        "login/",
        LoginAPIView.as_view(),
        name="login"
    ),

    path(
        "profile/",
        ProfileAPIView.as_view(),
        name="profile"
    ),
]