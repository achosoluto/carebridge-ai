"""
Core views for CareBridge AI system.
Contains essential API endpoints and utilities.
"""
from django.http import JsonResponse


def sentry_test(request):
    """Test Sentry error tracking"""
    division_by_zero = 1 / 0  # This will trigger an error
    return JsonResponse({'status': 'ok'})