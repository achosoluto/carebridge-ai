from django.db import models
from django.utils.translation import gettext_lazy as _

class Patient(models.Model):
    class Language(models.TextChoices):
        JAPANESE = 'JA', _('Japanese')
        CHINESE = 'ZH', _('Chinese')
        KOREAN = 'KO', _('Korean')
        ENGLISH = 'EN', _('English')

    name = models.CharField(max_length=100)
    language = models.CharField(
        max_length=2,
        choices=Language.choices,
        default=Language.JAPANESE,
    )
    contact_info = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_language_display()})"


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    is_public = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Dr. {self.name} - {self.specialty}"


class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        CONFIRMED = 'CONFIRMED', _('Confirmed')
        COMPLETED = 'COMPLETED', _('Completed')
        CANCELLED = 'CANCELLED', _('Cancelled')

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, related_name='appointments')
    datetime = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.name} with {self.doctor.name} on {self.datetime}"


class Message(models.Model):
    class SenderType(models.TextChoices):
        PATIENT = 'PATIENT', _('Patient')
        STAFF = 'STAFF', _('Staff')

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='messages')
    sender_type = models.CharField(max_length=10, choices=SenderType.choices)
    content = models.TextField()
    language = models.CharField(max_length=10, default='en') # stores 'ja', 'zh', 'ko' etc.
    translated_content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender_type}: {self.content[:20]}..."
