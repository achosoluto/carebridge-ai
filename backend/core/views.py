from rest_framework import viewsets, permissions
from .models import Patient, Doctor, Appointment, Message
from .serializers import PatientSerializer, DoctorSerializer, AppointmentSerializer, MessageSerializer, serializers
from .services import translation_service

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by('-created_at')
    serializer_class = PatientSerializer
    # permission_classes = [permissions.IsAuthenticated] # Commented out for easier testing in early dev

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all().order_by('datetime')
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        """Allows filtering by date or status"""
        queryset = super().get_queryset()
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('created_at')
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        """Auto-translate message on creation"""
        message = serializer.save()
        
        # Determine target language
        target_lang = 'en' # Default fallback
        if message.sender_type == 'STAFF':
            target_lang = message.patient.language
        else:
            target_lang = 'ko' # Staff reads in Korean (or EN as per proto)
            # Spec says: "Responds in Korean (auto-translated to patient's language)"
            # "Staff logs in... Sees translated patient messages"
            # So Patient (JA) -> Staff (KO)
            # Staff (KO) -> Patient (JA)
            
        # If content is provided but no translated content
        if message.content and not message.translated_content:
            translated = translation_service.translate_text(
                message.content, 
                target_language=target_lang.lower()
            )
            message.translated_content = translated
            message.save()
