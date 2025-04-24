from accounts.api.v1 import views
from django.urls import path, include

#  from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    # profile
    path("profile/", views.ProfileApiView.as_view(), name="profile"),
    # user activation
    path(
        "activation/conform/<str:token>",
        views.UserVerification.as_view(),
        name="UserVerification",
    ),
    path(
        "activation/resend/",
        views.ResendUserVerification.as_view(),
        name="ResendUserVerification",
    ),
    path(
        "password/confirm/<str:token>",
        views.PasswordRestLink.as_view(),
        name="password-rest",
    ),
]
