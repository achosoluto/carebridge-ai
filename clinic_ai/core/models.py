"""
Core domain models for the Hospital & Clinic Patient Management System.
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