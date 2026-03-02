from django.urls import path, include
from .views import *

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("register/", register, name="register"),
    path("verify-otp/", verify_otp, name="verify_otp"),
    path("profile/", profile, name="profile"),
]