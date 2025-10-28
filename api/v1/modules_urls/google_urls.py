from django.urls import path

from ..views.google_views import verify_captcha

urlpatterns = [
    path("verify-captcha-token", verify_captcha),
]
