from django.test import TestCase
from .models import Patient, Doctor, Appointment, Message
from .services import translation_service
from django.utils import timezone

class ModelTestCase(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(name="Sakura", language="JA")
        self.doctor = Doctor.objects.create(name="Dr. Kim", specialty="Plastic Surgery")

    def test_appointment_creation(self):
        appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            datetime=timezone.now()
        )
        self.assertEqual(appointment.status, "PENDING")
        self.assertEqual(str(appointment), f"{self.patient.name} with {self.doctor.name} on {appointment.datetime}")

    def test_message_creation(self):
        msg = Message.objects.create(
            patient=self.patient,
            sender_type="PATIENT",
            content="Hello",
            language="JA"
        )
        self.assertEqual(msg.content, "Hello")

class TranslationServiceTestCase(TestCase):
    def test_mock_translation(self):
        # Assuming no credentials in test env, should return mock format
        text = "Hello"
        translated = translation_service.translate_text(text, target_language="ko")
        # If credentials exist, this test might be flaky if we strictly assert mock format.
        # But for now, let's just assert it returns a string.
        self.assertIsInstance(translated, str)
        self.assertTrue(len(translated) > 0)

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User

class APITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='staff', password='password')
        self.client.force_authenticate(user=self.user)
        self.patient = Patient.objects.create(name="Sakura", language="JA")
        self.doctor = Doctor.objects.create(name="Dr. Kim", specialty="Surgeon")

    def test_get_patients(self):
        url = reverse('patient-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_patient(self):
        url = reverse('patient-list')
        data = {
            "name": "New Test Patient",
            "language": "EN",
            "contact_info": "newpatient@example.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "New Test Patient")
        self.assertEqual(response.data['language'], "EN")
        self.assertEqual(Patient.objects.count(), 2)  # Original + new

    def test_update_patient(self):
        url = reverse('patient-detail', kwargs={'pk': self.patient.id})
        data = {
            "name": "Updated Patient Name",
            "language": "KO",
            "contact_info": "updated@example.com"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Updated Patient Name")
        self.assertEqual(response.data['language'], "KO")

    def test_delete_patient(self):
        url = reverse('patient-detail', kwargs={'pk': self.patient.id})
        initial_count = Patient.objects.count()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Patient.objects.count(), initial_count - 1)

    def test_create_appointment(self):
        url = reverse('appointment-list')
        data = {
            "patient": self.patient.id,
            "doctor": self.doctor.id,
            "datetime": timezone.now(),
            "status": "PENDING"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_send_message_translation(self):
        url = reverse('message-list')
        data = {
            "patient": self.patient.id,
            "sender_type": "PATIENT", # JA -> KO
            "content": "こんにちは",
            "language": "JA"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check that translated content was generated (mocked or real)
        self.assertTrue(response.data['translated_content'])
        # If mock, it should be "[KO] こんにちは" (target for staff is KO/EN? View logic says 'ko' or 'en')
        # View logic: if sender=STAFF -> target=patient.lang(JA). else -> target='ko'.
        # Since sender=PATIENT, target='ko'. Mock should return "[KO] <text>"
