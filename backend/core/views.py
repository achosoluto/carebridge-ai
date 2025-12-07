from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Patient, Doctor, Appointment, Message
from .serializers import PatientSerializer, DoctorSerializer, AppointmentSerializer, MessageSerializer, PublicAppointmentSerializer
from .services import translation_service
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by('-created_at')
    serializer_class = PatientSerializer
    permission_classes = [permissions.AllowAny]  # Temporarily allow any for testing

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all().order_by('datetime')
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.AllowAny]  # Temporarily allow any for testing

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
    permission_classes = [permissions.AllowAny]  # Temporarily allow any for testing

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

class PublicDoctorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Doctor.objects.filter(is_public=True)
    serializer_class = DoctorSerializer
    permission_classes = [permissions.AllowAny]

class PublicAppointmentViewSet(viewsets.GenericViewSet, viewsets.mixins.CreateModelMixin):
    queryset = Appointment.objects.all()
    serializer_class = PublicAppointmentSerializer
    permission_classes = [permissions.AllowAny]

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)

    # For testing, hardcode testuser/testpass
    if username == 'testuser' and password == 'testpass':
        return Response({'token': 'testtoken123'})

    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
