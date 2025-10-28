from django.urls import path, include

urlpatterns = [
    path("google/", include("api.v1.modules_urls.google_urls")),
    path("user/", include("api.v1.modules_urls.user_urls")),
]
