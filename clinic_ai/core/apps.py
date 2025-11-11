"""
Core Django app configuration for CareBridge AI.
Integrates existing domain models with Django ORM.
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clinic_ai.core'
    verbose_name = 'CareBridge AI Core'
    
    def ready(self):
        """Import signals when the app is ready."""
        import clinic_ai.core.signals