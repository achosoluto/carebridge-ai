"""
Web Django app configuration for CareBridge AI.
Handles web interface and templates.
"""

from django.apps import AppConfig


class WebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clinic_ai.web'
    verbose_name = 'CareBridge AI Web Interface'