"""CareBridge AI URL Configuration
Main URL configuration that integrates all Django apps and APIs.
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from .views import ReactAppView
from clinic_ai.core.views import sentry_test

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('clinic_ai.api.urls')),  # API endpoints
    path('api/sentry-test/', sentry_test, name='sentry_test'),
    path('', ReactAppView.as_view()),  # Serve React App at root
    re_path(r'^(?:.*)/?$', ReactAppView.as_view()),  # Catch-all for React Router
]

# Serve media and static files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)