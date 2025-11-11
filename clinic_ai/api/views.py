"""API views for CareBridge AI."""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from datetime import datetime, timedelta
from .serializers import (
    PatientSerializer, MessageSerializer, AppointmentSerializer,
    StaffResponseSerializer, SystemMetricsSerializer,
    MessageProcessorSerializer
)
from clinic_ai.core.models import (
    Patient, Message, Appointment, StaffResponse, SystemMetrics
)
from clinic_ai.messaging.ai_service import OpenAIService, KeywordBasedAIService, CompositeAIService
from clinic_ai.messaging.translation import TranslationService, FallbackTranslationService


class PatientViewSet(viewsets.ModelViewSet):
    """API endpoint for managing patients."""
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = []  # Allow access for now


class MessageViewSet(viewsets.ModelViewSet):
    """API endpoint for managing messages."""
    queryset = Message.objects.select_related('patient').all()
    serializer_class = MessageSerializer
    permission_classes = []  # Allow access for now
    
    def get_queryset(self):
        queryset = super().get_queryset()
        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        return queryset


class AppointmentViewSet(viewsets.ModelViewSet):
    """API endpoint for managing appointments."""
    queryset = Appointment.objects.select_related('patient', 'approved_by').all()
    serializer_class = AppointmentSerializer
    permission_classes = []  # Allow access for now


class StaffResponseViewSet(viewsets.ModelViewSet):
    """API endpoint for managing staff responses."""
    queryset = StaffResponse.objects.select_related('message', 'staff_user').all()
    serializer_class = StaffResponseSerializer
    permission_classes = []  # Allow access for now


class SystemMetricsViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for viewing system metrics."""
    queryset = SystemMetrics.objects.all()
    serializer_class = SystemMetricsSerializer
    permission_classes = []  # Allow access for now
    
    @action(detail=False)
    def summary(self, request):
        """Get metrics summary for the last 30 days."""
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_metrics = SystemMetrics.objects.filter(date__gte=thirty_days_ago)
        
        summary_data = {
            'total_messages': recent_metrics.aggregate(
                total=Count('id')
            )['total'],
            'ai_handled': recent_metrics.aggregate(
                ai=Count('id', filter=Q(ai_handled_messages__gt=0))
            )['ai'],
            'human_required': recent_metrics.aggregate(
                human=Count('id', filter=Q(human_needed_messages__gt=0))
            )['human'],
            'completed_appointments': recent_metrics.aggregate(
                completed=Count('id', filter=Q(completed_appointments__gt=0))
            )['completed'],
        }
        return Response(summary_data)


class MessageProcessorView(APIView):
    """API endpoint for processing messages from external channels."""
    serializer_class = MessageProcessorSerializer
    
    def post(self, request):
        """Process incoming message from external channel."""
        serializer = MessageProcessorSerializer(data=request.data)
        if serializer.is_valid():
            # Import message processing functionality
            from clinic_ai.messaging.handlers import MessageProcessor
            from clinic_ai.messaging.translation import TranslationService
            from clinic_ai.messaging.ai_service import CompositeAIService
            from clinic_ai.core.interfaces import ConfigurationService
            
            # Create simple config service for now
            class SimpleConfigService(ConfigurationService):
                def get_api_key(self, service_name):
                    return 'test_key'
                    
                def get_setting(self, key, default=None):
                    return default
                    
                def is_feature_enabled(self, feature_name):
                    return True
            
            # Initialize services
            config_service = SimpleConfigService()
            
            # Create proper AI services
            primary_ai = OpenAIService(config_service)
            fallback_ai = KeywordBasedAIService()
            ai_service = CompositeAIService(primary_ai, fallback_ai)
            
            # Create translation service with fallback
            from clinic_ai.messaging.translation import FallbackTranslationService, SimpleLanguageDetector
            from clinic_ai.core.cache import SimpleCache
            
            # Create a simple translator that doesn't use external APIs
            class SimpleTranslator:
                def translate(self, text, from_lang, to_lang):
                    return text  # Return original text for now
                
                def get_supported_languages(self):
                    return ['ko', 'en', 'zh', 'ja']
            
            translator = FallbackTranslationService(SimpleTranslator(), SimpleLanguageDetector())
            
            processor = MessageProcessor(ai_service, translator, {})
            
            # Process the message
            result = processor.process_message(serializer.validated_data)
            return Response(result)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HealthCheckView(APIView):
    """API endpoint for health checks."""
    
    def get(self, request):
        """Return health check information."""
        try:
            # Test database connection
            db_healthy = Patient.objects.exists()
            
            return Response({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'services': {
                    'database': 'healthy' if db_healthy else 'unhealthy',
                    'redis': 'not_configured',  # Placeholder
                    'ai_service': 'not_configured'  # Placeholder
                }
            })
        except Exception as e:
            return Response({
                'status': 'unhealthy',
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)