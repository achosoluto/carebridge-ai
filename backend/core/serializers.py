from rest_framework import serializers
from .models import Patient, Doctor, Appointment, Message

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)

    class Meta:
        model = Appointment
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)

    class Meta:
        model = Message
        fields = '__all__'

class PublicAppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(write_only=True)
    patient_contact = serializers.CharField(write_only=True)
    patient_language = serializers.ChoiceField(choices=Patient.Language.choices, write_only=True)

    class Meta:
        model = Appointment
        fields = ['doctor', 'datetime', 'patient_name', 'patient_contact', 'patient_language']

    def create(self, validated_data):
        patient_name = validated_data.pop('patient_name')
        patient_contact = validated_data.pop('patient_contact')
        patient_language = validated_data.pop('patient_language')

        # Create new patient record for the booking
        patient = Patient.objects.create(
            name=patient_name,
            contact_info=patient_contact,
            language=patient_language
        )
        
        appointment = Appointment.objects.create(patient=patient, **validated_data)
        return appointment
