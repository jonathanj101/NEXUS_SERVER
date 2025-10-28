from rest_framework.throttling import AnonRateThrottle
import logging


class GetInContactAPIThrottle(AnonRateThrottle):
    scope = "get_in_contact_rate"
    rate = "500/day"

    def allow_request(self, request, view):
        is_allowed = super().allow_request(request, view)
        # Log if throttling is being triggered
        logging.info(f"Throttle check for {request}: Allowed = {is_allowed}")
        return is_allowed


class VerifyAuthorizedIPThrottle(AnonRateThrottle):
    scope = "verify_authorized_ip"
    rate = "10/day"

    def allow_request(self, request, view):
        is_allowed = super().allow_request(request, view)
        # Log if throttling is being triggered
        logging.info(f"Throttle check for {request}: Allowed = {is_allowed}")
        return is_allowed


class VerifyTokenThrottle(AnonRateThrottle):
    scope = "verify_token"
    rate = "500/day"

    def allow_request(self, request, view):
        is_allowed = super().allow_request(request, view)
        # Log if throttling is being triggered
        logging.info(f"Throttle check for {request}: Allowed = {is_allowed}")
        return is_allowed
