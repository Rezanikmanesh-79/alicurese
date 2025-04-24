from django.urls import path, include

urlpatterns = [
    path("", include("accounts.api.v1.urls.profile")),
    path("profile/", include("accounts.api.v1.urls.auth")),
]
