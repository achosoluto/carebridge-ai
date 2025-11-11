"""Core Django admin configuration for CareBridge AI models."""

from django.contrib import admin
from .models import Patient, Message, Appointment, StaffResponse, SystemMetrics


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('phone', 'name', 'preferred_language', 'created_at', 'updated_at')
    list_filter = ('preferred_language', 'created_at', 'updated_at')
    search_fields = ('phone', 'name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('patient', 'direction', 'channel', 'is_ai_handled', 'needs_human', 'confidence_score', 'created_at')
    list_filter = ('direction', 'channel', 'is_ai_handled', 'needs_human', 'created_at')
    search_fields = ('patient__phone', 'patient__name', 'content')
    readonly_fields = ('created_at', 'updated_at')
    fields = ('patient', 'content', 'direction', 'channel', 'is_ai_handled', 'needs_human', 'confidence_score')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'procedure', 'scheduled_at', 'status', 'approved_by', 'created_at')
    list_filter = ('status', 'scheduled_at', 'created_at')
    search_fields = ('patient__phone', 'patient__name', 'doctor', 'procedure')
    readonly_fields = ('created_at', 'updated_at')
    fields = ('patient', 'doctor', 'procedure', 'scheduled_at', 'status', 'notes', 'approved_by')


@admin.register(StaffResponse)
class StaffResponseAdmin(admin.ModelAdmin):
    list_display = ('message', 'staff_user', 'response_time', 'satisfaction_rating', 'created_at')
    list_filter = ('satisfaction_rating', 'created_at')
    search_fields = ('staff_user__username', 'content', 'message__content')
    readonly_fields = ('created_at', 'updated_at')
    fields = ('message', 'staff_user', 'content', 'response_time', 'satisfaction_rating')


@admin.register(SystemMetrics)
class SystemMetricsAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_messages', 'ai_handled_messages', 'human_needed_messages', 'completed_appointments')
    list_filter = ('date',)
    readonly_fields = ('created_at', 'updated_at')
    fields = ('date', 'total_messages', 'ai_handled_messages', 'human_needed_messages', 'completed_appointments', 
              'average_response_time', 'patient_satisfaction_avg')