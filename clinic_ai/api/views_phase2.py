"""
Phase 2 API views for CareBridge AI.
Advanced features: Translation, Scheduling Optimization, Notifications.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Avg, Count, Q
from datetime import datetime, timedelta
import logging

from .serializers import (
    TranslationHistorySerializer, TranslateRequestSerializer,
    MedicalTerminologySerializer, DoctorSerializer, DoctorAvailabilitySerializer,
    ProcedureTypeSerializer, AppointmentWaitlistSerializer,
    SchedulingOptimizationSerializer, AppointmentReminderSerializer,
    AvailableSlotsRequestSerializer, AppointmentOptimizationRequestSerializer,
    WaitlistRequestSerializer
)
from clinic_ai.core.models import (
    TranslationHistory, MedicalTerminology, Doctor, DoctorAvailability,
    ProcedureType, AppointmentWaitlist, SchedulingOptimization,
    AppointmentReminder, Appointment, Patient
)

logger = logging.getLogger(__name__)


class TranslationViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for translation history."""
    queryset = TranslationHistory.objects.all()
    serializer_class = TranslationHistorySerializer
    permission_classes = []

    @action(detail=False, methods=['post'])
    def translate(self, request):
        """
        Translate text using Google Translate API.
        
        POST /api/translations/translate/
        {
            "text": "안녕하세요",
            "target_language": "en",
            "source_language": "auto",
            "message_id": 123
        }
        """
        serializer = TranslateRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            from clinic_ai.messaging.translation_enhanced import (
                EnhancedGoogleTranslateService, EnhancedTranslationService
            )
            from clinic_ai.core.interfaces import ConfigurationService
            
            # Simple config service
            class SimpleConfig(ConfigurationService):
                def get_api_key(self, service_name):
                    from django.conf import settings
                    return settings.CLINIC_AI.get('GOOGLE_TRANSLATE_API_KEY', 'test_key')
                
                def get_setting(self, key, default=None):
                    return default
                
                def is_feature_enabled(self, feature_name):
                    return True

            # Initialize translation service
            config = SimpleConfig()
            translator = EnhancedGoogleTranslateService(config)
            translation_service = EnhancedTranslationService(translator)

            # Perform translation
            result = translation_service.translate_message(
                text=serializer.validated_data['text'],
                target_lang=serializer.validated_data['target_language'],
                source_lang=serializer.validated_data.get('source_language'),
                message_id=serializer.validated_data.get('message_id')
            )

            return Response(result)

        except Exception as e:
            logger.error(f"Translation error: {e}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Get translation statistics.
        
        GET /api/translations/stats/?days=30
        """
        days = int(request.query_params.get('days', 30))
        
        try:
            from clinic_ai.messaging.translation_enhanced import EnhancedTranslationService
            from clinic_ai.messaging.translation import SimpleLanguageDetector
            
            # Create minimal service for stats
            class DummyTranslator:
                def translate(self, text, from_lang, to_lang):
                    return text
                def get_supported_languages(self):
                    return ['ko', 'en', 'zh', 'ja']
            
            service = EnhancedTranslationService(DummyTranslator(), SimpleLanguageDetector())
            stats = service.get_translation_stats(days=days)
            
            return Response(stats)
        
        except Exception as e:
            logger.error(f"Error getting translation stats: {e}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def rate_quality(self, request, pk=None):
        """
        Rate translation quality.
        
        POST /api/translations/{id}/rate_quality/
        {
            "quality_score": 0.95
        }
        """
        translation = self.get_object()
        quality_score = request.data.get('quality_score')
        
        if quality_score is None or not (0 <= quality_score <= 1):
            return Response(
                {'error': 'quality_score must be between 0 and 1'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        translation.quality_score = quality_score
        translation.save()
        
        return Response({
            'success': True,
            'translation_id': translation.id,
            'quality_score': quality_score
        })


class MedicalTerminologyViewSet(viewsets.ModelViewSet):
    """API endpoint for medical terminology management."""
    queryset = MedicalTerminology.objects.all()
    serializer_class = MedicalTerminologySerializer
    permission_classes = []

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset.order_by('-usage_count')

    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get list of all medical term categories."""
        categories = MedicalTerminology.objects.values_list(
            'category', flat=True
        ).distinct()
        return Response({'categories': list(categories)})

    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Search medical terminology.
        
        GET /api/medical-terms/search/?q=surgery&lang=en
        """
        query = request.query_params.get('q', '')
        lang = request.query_params.get('lang', 'en')
        
        if not query:
            return Response({'results': []})
        
        # Search in appropriate language field
        lang_field = f'term_{lang}'
        filter_kwargs = {f'{lang_field}__icontains': query}
        
        results = MedicalTerminology.objects.filter(
            **filter_kwargs
        )[:20]
        
        serializer = self.get_serializer(results, many=True)
        return Response({'results': serializer.data})


class DoctorViewSet(viewsets.ModelViewSet):
    """API endpoint for doctor management."""
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = []

    def get_queryset(self):
        queryset = super().get_queryset()
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        return queryset

    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        """Get doctor's availability schedule."""
        doctor = self.get_object()
        availability = DoctorAvailability.objects.filter(doctor=doctor)
        serializer = DoctorAvailabilitySerializer(availability, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def workload(self, request, pk=None):
        """Get doctor's current workload statistics."""
        doctor = self.get_object()
        
        # Get appointments for next 7 days
        today = timezone.now().date()
        next_week = today + timedelta(days=7)
        
        appointments = Appointment.objects.filter(
            doctor=doctor.name,
            scheduled_at__date__gte=today,
            scheduled_at__date__lte=next_week,
            status__in=['pending', 'confirmed']
        )
        
        daily_counts = {}
        for appt in appointments:
            date_str = appt.scheduled_at.date().isoformat()
            daily_counts[date_str] = daily_counts.get(date_str, 0) + 1
        
        return Response({
            'doctor_id': doctor.id,
            'doctor_name': doctor.name,
            'max_daily_appointments': doctor.max_daily_appointments,
            'upcoming_appointments': appointments.count(),
            'daily_breakdown': daily_counts
        })


class DoctorAvailabilityViewSet(viewsets.ModelViewSet):
    """API endpoint for doctor availability management."""
    queryset = DoctorAvailability.objects.all()
    serializer_class = DoctorAvailabilitySerializer
    permission_classes = []


class ProcedureTypeViewSet(viewsets.ModelViewSet):
    """API endpoint for procedure type management."""
    queryset = ProcedureType.objects.all()
    serializer_class = ProcedureTypeSerializer
    permission_classes = []

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search procedure types by name."""
        query = request.query_params.get('q', '')
        lang = request.query_params.get('lang', 'en')
        
        if not query:
            return Response({'results': []})
        
        # Search in name and localized names
        results = ProcedureType.objects.filter(
            Q(name__icontains=query) |
            Q(name_ko__icontains=query) |
            Q(name_zh__icontains=query) |
            Q(name_ja__icontains=query)
        )[:20]
        
        serializer = self.get_serializer(results, many=True)
        return Response({'results': serializer.data})


class SchedulingOptimizationView(APIView):
    """API endpoint for advanced scheduling optimization."""
    permission_classes = []

    def post(self, request):
        """
        Get optimized appointment recommendations.
        
        POST /api/scheduling/optimize/
        {
            "patient_id": 1,
            "doctor_id": 2,
            "procedure_type_id": 3,
            "requested_time": "2025-11-15T10:00:00Z",
            "preferences": {"preferred_time": "morning"}
        }
        """
        serializer = AppointmentOptimizationRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            from clinic_ai.messaging.scheduling_optimizer import AdvancedSchedulingOptimizer
            
            optimizer = AdvancedSchedulingOptimizer()
            data = serializer.validated_data
            
            # Get doctor
            doctor = Doctor.objects.get(id=data['doctor_id'])
            procedure_type = ProcedureType.objects.get(id=data['procedure_type_id'])
            
            # Find optimal slot
            optimal_result = optimizer.optimize_schedule([{
                'patient_id': data['patient_id'],
                'doctor': str(doctor.id),  # Pass doctor ID as string
                'procedure': str(data['procedure_type_id']),  # Pass procedure ID as string
                'requested_time': data['requested_time']
            }])
            
            if optimal_result:
                return Response({
                    'success': True,
                    'optimization': optimal_result[0]
                })
            else:
                return Response({
                    'success': False,
                    'message': 'No optimization available'
                })

        except Doctor.DoesNotExist:
            return Response(
                {'error': 'Doctor not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Optimization error: {e}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AvailableSlotsView(APIView):
    """API endpoint for finding available appointment slots."""
    permission_classes = []

    def post(self, request):
        """
        Find available appointment slots.
        
        POST /api/scheduling/available-slots/
        {
            "doctor_id": 1,
            "start_date": "2025-11-15",
            "end_date": "2025-11-22",
            "preferred_time": "morning"
        }
        """
        serializer = AvailableSlotsRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            from clinic_ai.messaging.scheduling_optimizer import AdvancedSchedulingOptimizer
            
            optimizer = AdvancedSchedulingOptimizer()
            data = serializer.validated_data
            
            # Get doctor
            doctor = Doctor.objects.get(id=data['doctor_id'])
            
            # Build date range
            start_datetime = timezone.make_aware(
                datetime.combine(data['start_date'], datetime.min.time())
            )
            end_datetime = timezone.make_aware(
                datetime.combine(data['end_date'], datetime.max.time())
            )
            
            # Build preferences
            preferences = {}
            if 'preferred_time' in data and data['preferred_time'] != 'any':
                preferences['preferred_time'] = data['preferred_time']
            
            # Find available slots
            slots = optimizer.find_available_slots(
                doctor=str(doctor.id),  # Pass doctor ID as string
                date_range=(start_datetime, end_datetime),
                preferences=preferences
            )
            
            return Response({
                'doctor_id': doctor.id,
                'doctor_name': doctor.name,
                'available_slots': [slot.isoformat() for slot in slots],
                'total_slots': len(slots)
            })

        except Doctor.DoesNotExist:
            return Response(
                {'error': 'Doctor not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error finding slots: {e}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AppointmentWaitlistViewSet(viewsets.ModelViewSet):
    """API endpoint for appointment waitlist management."""
    queryset = AppointmentWaitlist.objects.all()
    serializer_class = AppointmentWaitlistSerializer
    permission_classes = []

    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset.order_by('-priority_score', 'created_at')

    @action(detail=False, methods=['post'])
    def add(self, request):
        """
        Add patient to waitlist.
        
        POST /api/waitlist/add/
        """
        serializer = WaitlistRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            from clinic_ai.messaging.scheduling_optimizer import AdvancedSchedulingOptimizer
            
            optimizer = AdvancedSchedulingOptimizer()
            data = serializer.validated_data
            
            result = optimizer.add_to_waitlist(
                patient_id=data['patient_id'],
                doctor_id=data['doctor_id'],
                procedure_type_id=data['procedure_type_id'],
                preferences={
                    'preferred_date': data['preferred_date'],
                    'time_start': data['preferred_time_start'],
                    'time_end': data['preferred_time_end']
                }
            )
            
            return Response(result)

        except Exception as e:
            logger.error(f"Waitlist error: {e}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def process_notifications(self, request):
        """Process waitlist and send notifications for available slots."""
        try:
            from clinic_ai.messaging.scheduling_optimizer import AdvancedSchedulingOptimizer
            
            optimizer = AdvancedSchedulingOptimizer()
            count = optimizer.process_waitlist_notifications()
            
            return Response({
                'success': True,
                'notifications_sent': count
            })

        except Exception as e:
            logger.error(f"Waitlist processing error: {e}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AppointmentReminderViewSet(viewsets.ModelViewSet):
    """API endpoint for appointment reminder management."""
    queryset = AppointmentReminder.objects.all()
    serializer_class = AppointmentReminderSerializer
    permission_classes = []

    @action(detail=False, methods=['post'])
    def schedule(self, request):
        """
        Schedule appointment reminder.
        
        POST /api/reminders/schedule/
        {
            "appointment_id": 1,
            "hours_before": 24
        }
        """
        appointment_id = request.data.get('appointment_id')
        hours_before = request.data.get('hours_before', 24)
        
        if not appointment_id:
            return Response(
                {'error': 'appointment_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            from clinic_ai.messaging.notification_service import MultiChannelNotificationService
            
            notification_service = MultiChannelNotificationService()
            success = notification_service.schedule_reminder(
                appointment_id=appointment_id,
                hours_before=hours_before
            )
            
            return Response({
                'success': success,
                'appointment_id': appointment_id,
                'hours_before': hours_before
            })

        except Exception as e:
            logger.error(f"Reminder scheduling error: {e}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def process_pending(self, request):
        """Process and send all pending reminders."""
        try:
            from clinic_ai.messaging.notification_service import MultiChannelNotificationService
            
            notification_service = MultiChannelNotificationService()
            count = notification_service.process_pending_reminders()
            
            return Response({
                'success': True,
                'reminders_sent': count
            })

        except Exception as e:
            logger.error(f"Reminder processing error: {e}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )