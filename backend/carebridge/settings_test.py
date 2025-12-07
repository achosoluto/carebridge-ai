"""
Test settings for running tests with SQLite
"""
from .settings import *
from core.test_utils import MockTranslationService

# Use SQLite for testing to avoid Docker network issues
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_test.sqlite3',
    }
}

# Override REST_FRAMEWORK settings for testing
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'core.test_utils.MockStaffAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}

TRANSLATION_SERVICE_CLASS = 'core.test_utils.MockTranslationService'