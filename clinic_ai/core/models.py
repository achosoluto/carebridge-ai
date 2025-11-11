"""
Core domain models for CareBridge AI - Hospital & Clinic Patient Management System.
Following SOLID principles with composition over inheritance.
"""

from django.db import models
from django.contrib.auth.models import User


class BaseEntity(models.Model):
    """
    Abstract base entity with common auditing fields.
    Composition approach for reusable audit functionality.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Patient(BaseEntity):
    """
    Patient entity representing system users.
    Encapsulated patient data with language preference management.
    """
    SUPPORTED_LANGUAGES = [
        ('ko', 'Korean'),
        ('en', 'English'),
        ('zh', 'Chinese'),
        ('ja', 'Japanese'),
    ]

    phone = models.CharField(max_length=20, unique=True, help_text="Patient's phone number as primary identifier")
    name = models.CharField(max_length=100, blank=True, help_text="Optional patient name")
    preferred_language = models.CharField(max_length=2, choices=SUPPORTED_LANGUAGES, default='ko')

    def __str__(self):
        return f"{self.name or 'Unknown'} ({self.phone})"

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"


class Message(BaseEntity):
    """
    Message entity for all communication interactions.
    Single responsibility: store message data with audit trail.
    """
    DIRECTION_CHOICES = [
        ('incoming', 'Incoming'),
        ('outgoing', 'Outgoing'),
    ]

    CHANNEL_CHOICES = [
        ('kakao', 'KakaoTalk'),
        ('wechat', 'WeChat'),
        ('line', 'LINE'),
        ('sms', 'SMS'),
        ('phone', 'Phone'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField(help_text="Message content")
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES)
    channel = models.CharField(max_length=10, choices=CHANNEL_CHOICES)
    is_ai_handled = models.BooleanField(default=False, help_text="Whether AI processed this message")
    needs_human = models.BooleanField(default=False, help_text="Whether human intervention required")
    confidence_score = models.FloatField(null=True, blank=True, help_text="AI confidence in handling (0-1)")

    def __str__(self):
        return f"{self.direction} message from {self.patient}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Message"
        verbose_name_plural = "Messages"


class Appointment(BaseEntity):
    """
    Appointment entity for scheduling management.
    Encapsulated booking data with status tracking.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending Staff Approval'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.CharField(max_length=100, help_text="Doctor's name")
    procedure = models.CharField(max_length=200, help_text="Medical procedure type")
    scheduled_at = models.DateTimeField(help_text="Appointment date and time")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, help_text="Additional appointment notes")
    approved_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='approved_appointments')

    def __str__(self):
        return f"{self.patient} - {self.doctor} - {self.scheduled_at}"

    class Meta:
        ordering = ['scheduled_at']
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"


class StaffResponse(BaseEntity):
    """
    Staff response entity for tracking human interventions.
    Links to original message with response details.
    """
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='staff_responses')
    staff_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses')
    content = models.TextField(help_text="Staff response content")
    response_time = models.DurationField(null=True, blank=True, help_text="Time to respond")
    satisfaction_rating = models.IntegerField(null=True, blank=True, help_text="Patient satisfaction rating 1-5")

    def __str__(self):
        return f"Response by {self.staff_user} to {self.message}"

    class Meta:
        verbose_name = "Staff Response"
        verbose_name_plural = "Staff Responses"


class SystemMetrics(BaseEntity):
    """
    System performance metrics entity.
    Single responsibility: store operational KPIs.
    """
    date = models.DateField(help_text="Date of metrics")
    total_messages = models.IntegerField(default=0)
    ai_handled_messages = models.IntegerField(default=0)
    human_needed_messages = models.IntegerField(default=0)
    completed_appointments = models.IntegerField(default=0)
    average_response_time = models.DurationField(null=True, blank=True)
    patient_satisfaction_avg = models.FloatField(null=True, blank=True, help_text="Average satisfaction rating")

    def __str__(self):
        return f"Metrics for {self.date}"

    class Meta:
        ordering = ['-date']
        verbose_name = "System Metrics"
        verbose_name_plural = "System Metrics"


# ============================================================================
# PHASE 2: Advanced Features Models
# ============================================================================

class TranslationHistory(BaseEntity):
    """
    Translation history for audit and quality tracking.
    Stores all translation operations with quality metrics.
    """
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='translations', null=True, blank=True)
    source_text = models.TextField(help_text="Original text")
    translated_text = models.TextField(help_text="Translated text")
    source_language = models.CharField(max_length=10, help_text="Source language code")
    target_language = models.CharField(max_length=10, help_text="Target language code")
    translation_service = models.CharField(max_length=50, default='google', help_text="Translation service used")
    confidence_score = models.FloatField(null=True, blank=True, help_text="Translation confidence (0-1)")
    quality_score = models.FloatField(null=True, blank=True, help_text="Manual quality rating (0-1)")
    is_medical_terminology = models.BooleanField(default=False, help_text="Contains medical terms")
    processing_time_ms = models.IntegerField(null=True, blank=True, help_text="Translation time in milliseconds")
    
    def __str__(self):
        return f"{self.source_language} -> {self.target_language}: {self.source_text[:50]}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Translation History"
        verbose_name_plural = "Translation Histories"
        indexes = [
            models.Index(fields=['source_language', 'target_language']),
            models.Index(fields=['created_at']),
        ]


class MedicalTerminology(BaseEntity):
    """
    Medical terminology translations for accurate healthcare communication.
    Custom mappings for medical terms across languages.
    """
    term_en = models.CharField(max_length=200, help_text="English medical term")
    term_ko = models.CharField(max_length=200, blank=True, help_text="Korean translation")
    term_zh = models.CharField(max_length=200, blank=True, help_text="Chinese translation")
    term_ja = models.CharField(max_length=200, blank=True, help_text="Japanese translation")
    category = models.CharField(max_length=100, help_text="Medical category (e.g., procedure, diagnosis)")
    description = models.TextField(blank=True, help_text="Term description or context")
    usage_count = models.IntegerField(default=0, help_text="Number of times used")
    accuracy_rating = models.FloatField(default=1.0, help_text="Translation accuracy rating (0-1)")
    
    def __str__(self):
        return f"{self.term_en} ({self.category})"
    
    class Meta:
        verbose_name = "Medical Terminology"
        verbose_name_plural = "Medical Terminologies"
        indexes = [
            models.Index(fields=['term_en']),
            models.Index(fields=['category']),
        ]


class Doctor(BaseEntity):
    """
    Doctor entity for advanced scheduling.
    Manages doctor availability and specializations.
    """
    name = models.CharField(max_length=100, help_text="Doctor's full name")
    specialization = models.CharField(max_length=200, help_text="Medical specialization")
    email = models.EmailField(blank=True, help_text="Contact email")
    phone = models.CharField(max_length=20, blank=True, help_text="Contact phone")
    is_active = models.BooleanField(default=True, help_text="Currently active")
    max_daily_appointments = models.IntegerField(default=20, help_text="Maximum appointments per day")
    average_appointment_duration = models.DurationField(help_text="Average appointment duration")
    
    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"
    
    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"


class DoctorAvailability(BaseEntity):
    """
    Doctor availability schedule for intelligent booking.
    Defines when doctors are available for appointments.
    """
    WEEKDAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='availability_slots')
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES, help_text="Day of week (0=Monday)")
    start_time = models.TimeField(help_text="Availability start time")
    end_time = models.TimeField(help_text="Availability end time")
    is_available = models.BooleanField(default=True, help_text="Currently available")
    
    def __str__(self):
        return f"{self.doctor.name} - {self.get_weekday_display()} {self.start_time}-{self.end_time}"
    
    class Meta:
        verbose_name = "Doctor Availability"
        verbose_name_plural = "Doctor Availabilities"
        unique_together = ['doctor', 'weekday', 'start_time']


class ProcedureType(BaseEntity):
    """
    Medical procedure types with duration and requirements.
    Used for intelligent scheduling and resource allocation.
    """
    name = models.CharField(max_length=200, help_text="Procedure name")
    name_ko = models.CharField(max_length=200, blank=True, help_text="Korean name")
    name_zh = models.CharField(max_length=200, blank=True, help_text="Chinese name")
    name_ja = models.CharField(max_length=200, blank=True, help_text="Japanese name")
    description = models.TextField(blank=True, help_text="Procedure description")
    estimated_duration = models.DurationField(help_text="Estimated procedure duration")
    requires_equipment = models.TextField(blank=True, help_text="Required equipment (comma-separated)")
    preparation_time = models.DurationField(null=True, blank=True, help_text="Pre-procedure preparation time")
    recovery_time = models.DurationField(null=True, blank=True, help_text="Post-procedure recovery time")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Procedure Type"
        verbose_name_plural = "Procedure Types"


class AppointmentWaitlist(BaseEntity):
    """
    Waitlist for popular appointment slots.
    Manages patient queue for fully booked time slots.
    """
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('notified', 'Notified'),
        ('booked', 'Booked'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='waitlist_entries')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='waitlist_entries')
    procedure_type = models.ForeignKey(ProcedureType, on_delete=models.CASCADE, related_name='waitlist_entries')
    preferred_date = models.DateField(help_text="Preferred appointment date")
    preferred_time_start = models.TimeField(help_text="Preferred time range start")
    preferred_time_end = models.TimeField(help_text="Preferred time range end")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    priority_score = models.IntegerField(default=0, help_text="Priority score for queue ordering")
    notified_at = models.DateTimeField(null=True, blank=True, help_text="When patient was notified")
    expires_at = models.DateTimeField(null=True, blank=True, help_text="When waitlist entry expires")
    
    def __str__(self):
        return f"{self.patient} - {self.doctor} - {self.preferred_date}"
    
    class Meta:
        ordering = ['-priority_score', 'created_at']
        verbose_name = "Appointment Waitlist"
        verbose_name_plural = "Appointment Waitlists"


class SchedulingOptimization(BaseEntity):
    """
    Scheduling optimization tracking and preferences.
    Stores optimization results and patient preferences.
    """
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='optimization')
    original_scheduled_at = models.DateTimeField(help_text="Original requested time")
    optimized_scheduled_at = models.DateTimeField(help_text="AI-optimized time")
    optimization_score = models.FloatField(help_text="Optimization quality score (0-1)")
    wait_time_reduction_minutes = models.IntegerField(default=0, help_text="Estimated wait time reduction")
    patient_accepted = models.BooleanField(default=False, help_text="Patient accepted optimization")
    optimization_reason = models.TextField(blank=True, help_text="Reason for optimization")
    
    def __str__(self):
        return f"Optimization for {self.appointment}"
    
    class Meta:
        verbose_name = "Scheduling Optimization"
        verbose_name_plural = "Scheduling Optimizations"


class AppointmentReminder(BaseEntity):
    """
    Appointment reminder tracking.
    Manages automated reminder notifications.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    CHANNEL_CHOICES = [
        ('sms', 'SMS'),
        ('email', 'Email'),
        ('kakao', 'KakaoTalk'),
        ('wechat', 'WeChat'),
        ('line', 'LINE'),
    ]
    
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='reminders')
    scheduled_send_at = models.DateTimeField(help_text="When to send reminder")
    sent_at = models.DateTimeField(null=True, blank=True, help_text="When reminder was sent")
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES, default='sms')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message_content = models.TextField(help_text="Reminder message content")
    error_message = models.TextField(blank=True, help_text="Error details if failed")
    
    def __str__(self):
        return f"Reminder for {self.appointment} via {self.channel}"
    
    class Meta:
        ordering = ['scheduled_send_at']
        verbose_name = "Appointment Reminder"
        verbose_name_plural = "Appointment Reminders"