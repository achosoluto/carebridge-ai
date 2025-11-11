"""API serializers for CareBridge AI."""

from rest_framework import serializers
from clinic_ai.core.models import (
    Patient, Message, Appointment, StaffResponse, SystemMetrics,
    TranslationHistory, MedicalTerminology, Doctor, DoctorAvailability,
    ProcedureType, AppointmentWaitlist, SchedulingOptimization,
    AppointmentReminder
)


class PatientSerializer(serializers.ModelSerializer):
    """Serializer for Patient model."""
    
    class Meta:
        model = Patient
        fields = ['id', 'phone', 'name', 'preferred_language', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model."""
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    patient_phone = serializers.CharField(source='patient.phone', read_only=True)
    
    class Meta:
        model = Message
        fields = [
            'id', 'patient', 'patient_name', 'patient_phone', 'content', 
            'direction', 'channel', 'is_ai_handled', 'needs_human', 
            'confidence_score', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class AppointmentSerializer(serializers.ModelSerializer):
    """Serializer for Appointment model."""
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    patient_phone = serializers.CharField(source='patient.phone', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.username', read_only=True)
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'patient_name', 'patient_phone', 'doctor', 
            'procedure', 'scheduled_at', 'status', 'notes', 
            'approved_by', 'approved_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class StaffResponseSerializer(serializers.ModelSerializer):
    """Serializer for StaffResponse model."""
    staff_user_name = serializers.CharField(source='staff_user.username', read_only=True)
    message_preview = serializers.CharField(source='message.content', read_only=True)
    
    class Meta:
        model = StaffResponse
        fields = [
            'id', 'message', 'message_preview', 'staff_user', 'staff_user_name',
            'content', 'response_time', 'satisfaction_rating', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class SystemMetricsSerializer(serializers.ModelSerializer):
    """Serializer for SystemMetrics model."""
    
    class Meta:
        model = SystemMetrics
        fields = [
            'id', 'date', 'total_messages', 'ai_handled_messages', 
            'human_needed_messages', 'completed_appointments', 
            'average_response_time', 'patient_satisfaction_avg',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class MessageProcessorSerializer(serializers.Serializer):
    """Serializer for processing incoming messages."""
    channel = serializers.ChoiceField(choices=[
        ('kakao', 'KakaoTalk'),
        ('wechat', 'WeChat'),
        ('line', 'LINE'),
        ('sms', 'SMS'),
        ('phone', 'Phone'),
    ])
    recipient = serializers.CharField(max_length=100)
    content = serializers.CharField()
    timestamp = serializers.DateTimeField(required=False)
    
    def validate_recipient(self, value):
        """Validate recipient format."""
        # Basic validation - could be enhanced based on channel requirements
        if len(value) < 5:
            raise serializers.ValidationError("Recipient must be at least 5 characters long.")
        return value


# ============================================================================
# PHASE 2: Advanced Features Serializers
# ============================================================================

class TranslationHistorySerializer(serializers.ModelSerializer):
    """Serializer for Translation History."""
    
    class Meta:
        model = TranslationHistory
        fields = [
            'id', 'message', 'source_text', 'translated_text',
            'source_language', 'target_language', 'translation_service',
            'confidence_score', 'quality_score', 'is_medical_terminology',
            'processing_time_ms', 'created_at'
        ]
        read_only_fields = ['created_at']


class TranslateRequestSerializer(serializers.Serializer):
    """Serializer for translation requests."""
    text = serializers.CharField()
    target_language = serializers.ChoiceField(choices=['ko', 'en', 'zh', 'ja'])
    source_language = serializers.ChoiceField(
        choices=['ko', 'en', 'zh', 'ja', 'auto'],
        default='auto'
    )
    message_id = serializers.IntegerField(required=False)


class MedicalTerminologySerializer(serializers.ModelSerializer):
    """Serializer for Medical Terminology."""
    
    class Meta:
        model = MedicalTerminology
        fields = [
            'id', 'term_en', 'term_ko', 'term_zh', 'term_ja',
            'category', 'description', 'usage_count', 'accuracy_rating',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['usage_count', 'created_at', 'updated_at']


class DoctorSerializer(serializers.ModelSerializer):
    """Serializer for Doctor model."""
    
    class Meta:
        model = Doctor
        fields = [
            'id', 'name', 'specialization', 'email', 'phone',
            'is_active', 'max_daily_appointments', 'average_appointment_duration',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    """Serializer for Doctor Availability."""
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    weekday_display = serializers.CharField(source='get_weekday_display', read_only=True)
    
    class Meta:
        model = DoctorAvailability
        fields = [
            'id', 'doctor', 'doctor_name', 'weekday', 'weekday_display',
            'start_time', 'end_time', 'is_available',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ProcedureTypeSerializer(serializers.ModelSerializer):
    """Serializer for Procedure Type."""
    
    class Meta:
        model = ProcedureType
        fields = [
            'id', 'name', 'name_ko', 'name_zh', 'name_ja',
            'description', 'estimated_duration', 'requires_equipment',
            'preparation_time', 'recovery_time',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class AppointmentWaitlistSerializer(serializers.ModelSerializer):
    """Serializer for Appointment Waitlist."""
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    procedure_name = serializers.CharField(source='procedure_type.name', read_only=True)
    
    class Meta:
        model = AppointmentWaitlist
        fields = [
            'id', 'patient', 'patient_name', 'doctor', 'doctor_name',
            'procedure_type', 'procedure_name', 'preferred_date',
            'preferred_time_start', 'preferred_time_end', 'status',
            'priority_score', 'notified_at', 'expires_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['priority_score', 'notified_at', 'created_at', 'updated_at']


class SchedulingOptimizationSerializer(serializers.ModelSerializer):
    """Serializer for Scheduling Optimization."""
    
    class Meta:
        model = SchedulingOptimization
        fields = [
            'id', 'appointment', 'original_scheduled_at', 'optimized_scheduled_at',
            'optimization_score', 'wait_time_reduction_minutes',
            'patient_accepted', 'optimization_reason',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class AppointmentReminderSerializer(serializers.ModelSerializer):
    """Serializer for Appointment Reminder."""
    
    class Meta:
        model = AppointmentReminder
        fields = [
            'id', 'appointment', 'scheduled_send_at', 'sent_at',
            'channel', 'status', 'message_content', 'error_message',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['sent_at', 'created_at', 'updated_at']


class AvailableSlotsRequestSerializer(serializers.Serializer):
    """Serializer for available slots request."""
    doctor_id = serializers.IntegerField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    preferred_time = serializers.ChoiceField(
        choices=['morning', 'afternoon', 'evening', 'any'],
        default='any',
        required=False
    )


class AppointmentOptimizationRequestSerializer(serializers.Serializer):
    """Serializer for appointment optimization request."""
    patient_id = serializers.IntegerField()
    doctor_id = serializers.IntegerField()
    procedure_type_id = serializers.IntegerField()
    requested_time = serializers.DateTimeField()
    preferences = serializers.JSONField(required=False)


class WaitlistRequestSerializer(serializers.Serializer):
    """Serializer for waitlist addition request."""
    patient_id = serializers.IntegerField()
    doctor_id = serializers.IntegerField()
    procedure_type_id = serializers.IntegerField()
    preferred_date = serializers.DateField()
    preferred_time_start = serializers.TimeField()
    preferred_time_end = serializers.TimeField()