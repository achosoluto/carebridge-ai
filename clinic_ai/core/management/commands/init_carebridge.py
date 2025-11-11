"""Management command to initialize the CareBridge AI database."""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from clinic_ai.core.models import Patient, Message, Appointment, SystemMetrics
from django.utils import timezone
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Initialize the CareBridge AI database with sample data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-sample',
            action='store_true',
            help='Create sample patients and data',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Starting CareBridge AI database initialization...')
        )
        
        try:
            # Create superuser if doesn't exist
            self.create_superuser()
            
            if options.get('create_sample'):
                self.create_sample_data()
                self.stdout.write(
                    self.style.SUCCESS('Sample data created successfully!')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS('Database initialized. Use --create-sample to add sample data.')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error initializing database: {e}')
            )
            raise

    def create_superuser(self):
        """Create superuser if doesn't exist."""
        User = get_user_model()
        
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@carebridge-ai.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(
                self.style.SUCCESS('Created superuser: admin / admin123')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Superuser already exists')
            )

    def create_sample_data(self):
        """Create sample patients and test data."""
        
        # Create sample patients
        sample_patients = [
            {'phone': '+821012345678', 'name': '김환자', 'preferred_language': 'ko'},
            {'phone': '+821098765432', 'name': '이환자', 'preferred_language': 'ko'},
            {'phone': '+821055512345', 'name': 'John Smith', 'preferred_language': 'en'},
            {'phone': '+821033312345', 'name': '张伟', 'preferred_language': 'zh'},
            {'phone': '+821044412345', 'name': '田中太郎', 'preferred_language': 'ja'},
        ]
        
        created_patients = []
        for patient_data in sample_patients:
            patient, created = Patient.objects.get_or_create(
                phone=patient_data['phone'],
                defaults=patient_data
            )
            created_patients.append(patient)
            
        self.stdout.write(f'Created {len(created_patients)} sample patients')

        # Create sample messages
        sample_messages = [
            '안녕하세요, 예약을 하고 싶습니다.',
            'Could you help me book an appointment?',
            '你好，我想预约咨询。',
            'こんにちは、クレジットの掲載を依頼します。',
            '비용이 얼마인가요?',
            'What are the prices?',
        ]
        
        for i, patient in enumerate(created_patients[:3]):
            for j, content in enumerate(sample_messages[:2]):
                Message.objects.create(
                    patient=patient,
                    content=content,
                    direction='incoming' if j % 2 == 0 else 'outgoing',
                    channel='kakao' if patient.preferred_language == 'ko' else 'line',
                    is_ai_handled=j % 3 == 0,
                    confidence_score=random.uniform(0.5, 0.9)
                )
        
        self.stdout.write('Created sample messages')

        # Create sample appointments
        for patient in created_patients[:2]:
            Appointment.objects.create(
                patient=patient,
                doctor='Dr. Smith',
                procedure='Consultation',
                scheduled_at=timezone.now() + timedelta(days=random.randint(1, 30)),
                status=random.choice(['pending', 'confirmed', 'completed']),
                notes='Initial consultation appointment'
            )
        
        self.stdout.write('Created sample appointments')

        # Create system metrics for last 30 days
        today = datetime.now().date()
        for i in range(30):
            date = today - timedelta(days=i)
            SystemMetrics.objects.get_or_create(
                date=date,
                defaults={
                    'total_messages': random.randint(10, 100),
                    'ai_handled_messages': random.randint(5, 80),
                    'human_needed_messages': random.randint(1, 20),
                    'completed_appointments': random.randint(1, 5),
                    'average_response_time': timedelta(minutes=random.randint(2, 30)),
                    'patient_satisfaction_avg': round(random.uniform(3.5, 5.0), 2)
                }
            )
        
        self.stdout.write('Created system metrics for last 30 days')