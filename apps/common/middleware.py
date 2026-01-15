"""
Admin Action Tracking Middleware
Tracks all admin actions and logs them to the logging system
"""

import logging
from django.http import HttpRequest, HttpResponse
from django.contrib.admin.models import LogEntry, CHANGE, ADDITION, DELETION
from django.contrib.contenttypes.models import ContentType
from django.urls import resolve

logger = logging.getLogger('django')


class AdminActionTrackingMiddleware:
    """
    Middleware to track admin actions
    Note: Django admin already logs to its AdminLog table,
    but this provides additional structured logging
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)

        # Only track admin changes
        if request.path.startswith('/admin/') and request.method in ['POST', 'DELETE']:
            self._track_admin_request(request, response)

        return response

    def _track_admin_request(self, request: HttpRequest, response: HttpResponse):
        """Track admin POST/DELETE requests"""
        try:
            # Log the request
            logger.info(
                f"Admin Request: {request.method} {request.path} "
                f"by {request.user.username} - Status: {response.status_code}"
            )
        except Exception as e:
            logger.error(f"Error tracking admin request: {e}")

