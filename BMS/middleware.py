from django.http import JsonResponse
from constance import config
from rest_framework import status
from rest_framework.authentication import TokenAuthentication


class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.token_auth = TokenAuthentication()

    def __call__(self, request):
        user_auth = self.token_auth.authenticate(request)
        if user_auth:
            request.user, _ = user_auth

        if config.MAINTENANCE_MODE and not request.user.is_staff:
            return JsonResponse(
                {"detail": "The system is currently under maintenance. Please try again later."},
                status = status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return self.get_response(request)
