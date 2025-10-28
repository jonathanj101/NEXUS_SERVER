from django.urls import path
from ..views.user_views import contact_request

urlpatterns = [
    path("contact-request", contact_request),
]
