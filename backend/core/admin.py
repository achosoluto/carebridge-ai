from django.contrib import admin
from .models import Patient, Doctor, Appointment, Message

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'language', 'created_at')
    search_fields = ('name',)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'datetime', 'status')
    list_filter = ('status', 'datetime')
    date_hierarchy = 'datetime'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('patient', 'sender_type', 'created_at')
    list_filter = ('sender_type', 'language')
