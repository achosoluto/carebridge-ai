"""URL configuration for the CareBridge AI API."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PatientViewSet, MessageViewSet, AppointmentViewSet,
    StaffResponseViewSet, SystemMetricsViewSet,
    MessageProcessorView, HealthCheckView
)
from .views_phase2 import (
    TranslationViewSet, MedicalTerminologyViewSet,
    DoctorViewSet, DoctorAvailabilityViewSet, ProcedureTypeViewSet,
    AppointmentWaitlistViewSet, AppointmentReminderViewSet,
    SchedulingOptimizationView, AvailableSlotsView
)

# Create router and register viewsets
router = DefaultRouter()

# Phase 1 endpoints
router.register(r'patients', PatientViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'staff-responses', StaffResponseViewSet)
router.register(r'system-metrics', SystemMetricsViewSet)

# Phase 2 endpoints
router.register(r'translations', TranslationViewSet, basename='translation')
router.register(r'medical-terms', MedicalTerminologyViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'doctor-availability', DoctorAvailabilityViewSet)
router.register(r'procedure-types', ProcedureTypeViewSet)
router.register(r'waitlist', AppointmentWaitlistViewSet)
router.register(r'reminders', AppointmentReminderViewSet)

urlpatterns = [
    # API routes
    path('', include(router.urls)),
    
    # Phase 1 custom endpoints
    path('process-message/', MessageProcessorView.as_view(), name='process_message'),
    path('health/', HealthCheckView.as_view(), name='health_check'),
    
    # Phase 2 custom endpoints
    path('scheduling/optimize/', SchedulingOptimizationView.as_view(), name='scheduling_optimize'),
    path('scheduling/available-slots/', AvailableSlotsView.as_view(), name='available_slots'),
    
    # Message channel webhooks
    path('webhooks/kakao/', MessageProcessorView.as_view(), name='kakao_webhook'),
    path('webhooks/wechat/', MessageProcessorView.as_view(), name='wechat_webhook'),
    path('webhooks/line/', MessageProcessorView.as_view(), name='line_webhook'),
]