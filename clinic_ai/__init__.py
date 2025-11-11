"""
Core Django app for CareBridge AI.
Integrates with existing clinic_ai.core modules for domain models and interfaces.
"""

default_app_config = 'clinic_ai.core.apps.CoreConfig'

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)