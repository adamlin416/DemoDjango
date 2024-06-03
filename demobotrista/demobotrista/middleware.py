import json

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import (
    APIException,
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied,
)


class CustomErrorMiddleware(MiddlewareMixin):
    """Custom error handling middleware to follow RFC 7807."""

    def __call__(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        response = self.get_response(request)
        if response.status_code >= 400:
            response = self.format_error_response(request, response)
        else:
            response = self.format_success_response(request, response)
        return response

    def process_exception(self, request, exception):
        """Handle exceptions that doesn't raised as response and return a JSON response."""
        status_code = 500
        if hasattr(exception, "status_code"):
            status_code = exception.status_code

        response_data = {
            "type": "about:blank",
            "title": "Error" if status_code == 500 else exception.__class__.__name__,
            "status": status_code,
            "detail": str(exception),
            "instance": request.path,
        }
        return JsonResponse(response_data, status=status_code)

    def format_error_response(self, request, response):
        """Handle responses not 2XX and return a JSON follow RFC 7807."""
        try:
            response_data = json.loads(response.content)
            detail = (
                response_data
                if not isinstance(response_data, dict)
                else response_data.get("detail", response_data)
            )
            formatted_response = {
                "type": "about:blank",
                "title": response.reason_phrase,
                "status": response.status_code,
                "detail": detail,
                "instance": request.path,
            }
            return JsonResponse(formatted_response, status=response.status_code)
        except ValueError:
            pass  # Response content is not JSON, skip formatting

        return response

    def format_success_response(self, request, response):
        try:
            response_data = json.loads(response.content)
            formatted_response = {"data": response_data}
            return JsonResponse(formatted_response, status=response.status_code)
        except ValueError:
            pass  # Response content is not JSON, skip formatting

        return response
