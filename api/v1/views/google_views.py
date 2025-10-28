import os
import logging
import requests

from rest_framework.decorators import api_view
from rest_framework.response import Response

from dotenv import load_dotenv

# Loading environment variable
load_dotenv()


@api_view(["POST"])
def verify_captcha(request):
    print("api.views.verify_captcha()")
    print(os.environ["CAPTCHA_SECRET_KEY"])
    try:
        # print(json.loads(request.body))
        # token = json.loads(request.body)["token"]
        token = request.data.get("token", "")
        if not token:
            return Response({"message": "Missing Token", "status": False}, status=400)

        request_verification = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={"secret": os.environ["CAPTCHA_SECRET_KEY"], "response": token},
        )
        response = request_verification.json()
        print(type(response))
        if not response["success"]:
            return Response({"message": "Invalid token", "status": False}, status=409)
        return Response(
            {"message": "CAPTCHA Token Verified!", "status": True}, status=201
        )
    except Exception as error:
        print(f"An Invalid Request Error Occurred -> {error}")
        logging.error("An Invalid Request Error Occurred -> ", error)

        return Response({"message": "Invalid Request", "status": False}, status=405)
