import os
import logging
import requests
import datetime

from django.utils import timezone

from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from dotenv import load_dotenv

from mailer.services import send_templated_email

from ...utils.common.http_statuses import (
    SUCCESS_CODE,
    CONFLICT,
)

from ...utils.helpers.helpers import date_formatted

# Loading environment variables
load_dotenv()


@api_view(["POST"])
@throttle_classes([AnonRateThrottle])
def contact_request(request):
    print("api.views.user_views.contact_req()")
    name = request.data.get("fullName", "")
    email = request.data.get("email", "")
    message = request.data.get("message", "")

    if not name or not email or not message:
        return Response(
            {
                "message": "Please make sure name,email or message are not empty!",
                "status": False,
            },
            status=CONFLICT["CODE"],
        )
    send_templated_email(
        [email],
        "Thank you for contacting us!",
        "contact_autoresponse",
        context={
            "name": name,
            "email": email,
            "message": message,
            "submitted_at": date_formatted(timezone.now()),
            "support_email": "support@jjnexussolutions.com",
        },
    )

    send_templated_email(
        ["jjnexussolutionsllc@gmail.com"],
        "Contact Form Submssion!",
        "contact_notification",
        context={
            "name": name,
            "email": email,
            "message": message,
            "submitted_at": date_formatted(timezone.now()),
        },
    )
    # send_templated_email(
    #     ["jjnexussolutionsllc@gmail.com"],
    #     "Contact Form Submission!",
    #     "contact_notification",
    #     context={
    #         "name": name,
    #         "email": email,
    #         "message": message,
    #         "submitted_at": date_formatted(datetime.datetime.now()),
    #     },
    # )

    return Response(
        {
            "message": "We received your email and will contact you as soon as possible!",
            "status": True,
        },
        status=SUCCESS_CODE["STANDARD"],
    )
