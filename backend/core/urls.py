from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, DoctorViewSet, AppointmentViewSet, MessageViewSet, PublicDoctorViewSet, PublicAppointmentViewSet, login_view

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'public/doctors', PublicDoctorViewSet, basename='public-doctor')
router.register(r'public/appointments', PublicAppointmentViewSet, basename='public-appointment')

urlpatterns = router.urls + [
    path('login/', login_view, name='login'),
]
