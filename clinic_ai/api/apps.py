"""
API Django app configuration for CareBridge AI.
Handles REST API endpoints using Django REST Framework.
"""

from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clinic_ai.api'
    verbose_name = 'CareBridge AI API'