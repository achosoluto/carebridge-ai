"""
Messaging Django app configuration for CareBridge AI.
"""

from django.apps import AppConfig


class MessagingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clinic_ai.messaging'
    verbose_name = 'CareBridge AI Messaging'