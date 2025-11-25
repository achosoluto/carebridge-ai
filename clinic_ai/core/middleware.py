"""
Custom middleware for performance monitoring and logging
"""
import time
import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class PerformanceMonitoringMiddleware(MiddlewareMixin):
    """
    Monitor request/response performance and log slow requests
    """

    def process_request(self, request):
        """Start timer for request"""
        request._start_time = time.time()
        return None

    def process_response(self, request, response):
        """Log request duration and flag slow requests"""
        if hasattr(request, '_start_time'):
            duration = time.time() - request._start_time

            # Log all API requests
            logger.info(
                f"{request.method} {request.path} - {response.status_code} - {duration:.3f}s"
            )

            # Flag slow requests (>1 second)
            if duration > 1.0:
                logger.warning(
                    f"SLOW REQUEST: {request.method} {request.path} took {duration:.3f}s"
                )

            # Add performance header
            response['X-Response-Time'] = f"{duration:.3f}s"

        return response


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Log request details for debugging
    """

    def process_request(self, request):
        """Log incoming request details"""
        logger.debug(
            f"Request: {request.method} {request.path} "
            f"from {request.META.get('REMOTE_ADDR')}"
        )
        return None