from django.core.management.base import BaseCommand
from core.models import Patient, Doctor, Appointment, Message
from datetime import datetime, timedelta
import pytz

class Command(BaseCommand):
    help = 'Populate test data for staff testing scenarios'

    def handle(self, *args, **options):
        self.stdout.write('Populating test data...')

        # Create doctors
        doctors_data = [
            {'name': 'Dr. Jung Nam-ju', 'specialty': 'Plastic Surgery', 'is_public': True},
            {'name': 'Dr. Kim', 'specialty': 'Plastic Surgery', 'is_public': True},
            {'name': 'Dr. Park', 'specialty': 'Dermatology', 'is_public': True},
        ]

        doctors = {}
        for doctor_data in doctors_data:
            doctor, created = Doctor.objects.get_or_create(
                name=doctor_data['name'],
                defaults=doctor_data
            )
            doctors[doctor_data['name']] = doctor
            if created:
                self.stdout.write(f'Created doctor: {doctor.name}')

        # Create patients from test scenarios
        patients_data = [
            {'name': 'NAK*********', 'language': 'JA', 'contact_info': 'nak@example.com'},
            {'name': 'Huang Jia-yi', 'language': 'ZH', 'contact_info': 'huang@example.com'},
            {'name': 'Yang Jun\'ai', 'language': 'ZH', 'contact_info': 'yang@example.com'},
            {'name': 'Jiang Yihui', 'language': 'ZH', 'contact_info': 'jiang@example.com'},
        ]

        patients = {}
        for patient_data in patients_data:
            patient, created = Patient.objects.get_or_create(
                name=patient_data['name'],
                defaults=patient_data
            )
            patients[patient_data['name']] = patient
            if created:
                self.stdout.write(f'Created patient: {patient.name}')

        # Create appointments
        seoul_tz = pytz.timezone('Asia/Seoul')

        appointments_data = [
            {
                'patient': patients['NAK*********'],
                'doctor': doctors['Dr. Jung Nam-ju'],
                'datetime': seoul_tz.localize(datetime(2025, 11, 5, 17, 0)),  # Nov 5, 5:00 PM
                'status': 'PENDING'
            },
            {
                'patient': patients['Huang Jia-yi'],
                'doctor': doctors['Dr. Kim'],
                'datetime': seoul_tz.localize(datetime(2025, 3, 6, 10, 0)),  # March 6, 10:00 AM
                'status': 'CONFIRMED'
            },
            {
                'patient': patients['Yang Jun\'ai'],
                'doctor': doctors['Dr. Kim'],
                'datetime': seoul_tz.localize(datetime(2025, 3, 6, 10, 0)),  # March 6, 10:00 AM
                'status': 'CONFIRMED'
            },
            {
                'patient': patients['Jiang Yihui'],
                'doctor': doctors['Dr. Park'],
                'datetime': seoul_tz.localize(datetime(2025, 3, 6, 11, 30)),  # March 6, 11:30 AM
                'status': 'CONFIRMED'
            },
        ]

        for appt_data in appointments_data:
            appointment, created = Appointment.objects.get_or_create(
                patient=appt_data['patient'],
                doctor=appt_data['doctor'],
                datetime=appt_data['datetime'],
                defaults={'status': appt_data['status']}
            )
            if created:
                self.stdout.write(f'Created appointment: {appointment}')

        # Create sample messages
        messages_data = [
            {
                'patient': patients['NAK*********'],
                'sender_type': 'PATIENT',
                'content': '鼻のカウンセリングを検討しております。11月5日16:00以降で空いている時間はありますでしょうか?',
                'language': 'ja',
                'translated_content': '코 상담을 고려하고 있습니다. 11월 5일 16:00 이후에 가능한 시간이 있나요?'
            },
            {
                'patient': patients['NAK*********'],
                'sender_type': 'STAFF',
                'content': '11월 5일 17:00에 예약 가능합니다.',
                'language': 'ko',
                'translated_content': '11月5日17:00で予約可能です。'
            },
            {
                'patient': patients['NAK*********'],
                'sender_type': 'PATIENT',
                'content': '11月5日17:00でよろしくお願いいたします。',
                'language': 'ja',
                'translated_content': '11월 5일 17:00으로 부탁드립니다.'
            },
        ]

        for msg_data in messages_data:
            message, created = Message.objects.get_or_create(
                patient=msg_data['patient'],
                sender_type=msg_data['sender_type'],
                content=msg_data['content'],
                defaults={
                    'language': msg_data['language'],
                    'translated_content': msg_data['translated_content']
                }
            )
            if created:
                self.stdout.write(f'Created message: {message}')

        self.stdout.write(self.style.SUCCESS('Test data populated successfully!'))
        self.stdout.write('You can now test the staff scenarios:')
        self.stdout.write('1. Login with testuser/testpass')
        self.stdout.write('2. Check patients, appointments, and messages')
        self.stdout.write('3. Test appointment editing and status changes')
        self.stdout.write('4. Test patient record updates')