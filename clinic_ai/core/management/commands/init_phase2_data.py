"""
Management command to initialize Phase 2 sample data.
Creates doctors, procedure types, medical terminology, and availability schedules.
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import time, timedelta
from clinic_ai.core.models import (
    Doctor, DoctorAvailability, ProcedureType, MedicalTerminology
)


class Command(BaseCommand):
    help = 'Initialize Phase 2 sample data for CareBridge AI'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Initializing Phase 2 sample data...'))

        # Create Doctors
        self.stdout.write('Creating doctors...')
        doctors_data = [
            {
                'name': 'Dr. Kim Min-jun',
                'specialization': 'Plastic Surgery',
                'email': 'kim.minjun@carebridge.ai',
                'phone': '+82-10-1234-5678',
                'max_daily_appointments': 20,
                'average_appointment_duration': timedelta(minutes=30)
            },
            {
                'name': 'Dr. Park Ji-woo',
                'specialization': 'Dermatology',
                'email': 'park.jiwoo@carebridge.ai',
                'phone': '+82-10-2345-6789',
                'max_daily_appointments': 25,
                'average_appointment_duration': timedelta(minutes=20)
            },
            {
                'name': 'Dr. Lee Seo-yeon',
                'specialization': 'Cosmetic Surgery',
                'email': 'lee.seoyeon@carebridge.ai',
                'phone': '+82-10-3456-7890',
                'max_daily_appointments': 15,
                'average_appointment_duration': timedelta(minutes=45)
            },
        ]

        doctors = []
        for data in doctors_data:
            doctor, created = Doctor.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            doctors.append(doctor)
            if created:
                self.stdout.write(f'  ✓ Created doctor: {doctor.name}')
            else:
                self.stdout.write(f'  - Doctor already exists: {doctor.name}')

        # Create Doctor Availability
        self.stdout.write('Creating doctor availability schedules...')
        for doctor in doctors:
            # Monday to Friday: 9 AM - 6 PM
            for weekday in range(5):
                DoctorAvailability.objects.get_or_create(
                    doctor=doctor,
                    weekday=weekday,
                    start_time=time(9, 0),
                    defaults={
                        'end_time': time(18, 0),
                        'is_available': True
                    }
                )
            
            # Saturday: 9 AM - 1 PM
            DoctorAvailability.objects.get_or_create(
                doctor=doctor,
                weekday=5,
                start_time=time(9, 0),
                defaults={
                    'end_time': time(13, 0),
                    'is_available': True
                }
            )
            
            self.stdout.write(f'  ✓ Created availability for {doctor.name}')

        # Create Procedure Types
        self.stdout.write('Creating procedure types...')
        procedures_data = [
            {
                'name': 'Rhinoplasty',
                'name_ko': '코 성형',
                'name_zh': '鼻整形',
                'name_ja': '鼻形成',
                'description': 'Nose reshaping surgery',
                'estimated_duration': timedelta(hours=2),
                'preparation_time': timedelta(minutes=30),
                'recovery_time': timedelta(hours=1)
            },
            {
                'name': 'Double Eyelid Surgery',
                'name_ko': '쌍꺼풀 수술',
                'name_zh': '双眼皮手术',
                'name_ja': '二重まぶた手術',
                'description': 'Eyelid enhancement procedure',
                'estimated_duration': timedelta(minutes=45),
                'preparation_time': timedelta(minutes=15),
                'recovery_time': timedelta(minutes=30)
            },
            {
                'name': 'Botox Treatment',
                'name_ko': '보톡스 시술',
                'name_zh': '肉毒杆菌治疗',
                'name_ja': 'ボトックス治療',
                'description': 'Wrinkle reduction treatment',
                'estimated_duration': timedelta(minutes=20),
                'preparation_time': timedelta(minutes=10),
                'recovery_time': timedelta(minutes=15)
            },
            {
                'name': 'Facial Contouring',
                'name_ko': '안면 윤곽',
                'name_zh': '面部轮廓',
                'name_ja': '顔の輪郭形成',
                'description': 'Facial bone reshaping',
                'estimated_duration': timedelta(hours=3),
                'preparation_time': timedelta(hours=1),
                'recovery_time': timedelta(hours=2)
            },
            {
                'name': 'Laser Skin Treatment',
                'name_ko': '레이저 피부 치료',
                'name_zh': '激光皮肤治疗',
                'name_ja': 'レーザー皮膚治療',
                'description': 'Skin rejuvenation with laser',
                'estimated_duration': timedelta(minutes=30),
                'preparation_time': timedelta(minutes=10),
                'recovery_time': timedelta(minutes=20)
            },
        ]

        for data in procedures_data:
            procedure, created = ProcedureType.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created:
                self.stdout.write(f'  ✓ Created procedure: {procedure.name}')
            else:
                self.stdout.write(f'  - Procedure already exists: {procedure.name}')

        # Create Medical Terminology
        self.stdout.write('Creating medical terminology...')
        terms_data = [
            {
                'term_en': 'consultation',
                'term_ko': '상담',
                'term_zh': '咨询',
                'term_ja': '相談',
                'category': 'general',
                'description': 'Medical consultation or advice'
            },
            {
                'term_en': 'surgery',
                'term_ko': '수술',
                'term_zh': '手术',
                'term_ja': '手術',
                'category': 'procedure',
                'description': 'Surgical procedure'
            },
            {
                'term_en': 'anesthesia',
                'term_ko': '마취',
                'term_zh': '麻醉',
                'term_ja': '麻酔',
                'category': 'procedure',
                'description': 'Anesthesia administration'
            },
            {
                'term_en': 'recovery',
                'term_ko': '회복',
                'term_zh': '恢复',
                'term_ja': '回復',
                'category': 'general',
                'description': 'Post-procedure recovery'
            },
            {
                'term_en': 'appointment',
                'term_ko': '예약',
                'term_zh': '预约',
                'term_ja': '予約',
                'category': 'general',
                'description': 'Medical appointment'
            },
            {
                'term_en': 'prescription',
                'term_ko': '처방',
                'term_zh': '处方',
                'term_ja': '処方',
                'category': 'medication',
                'description': 'Medical prescription'
            },
            {
                'term_en': 'diagnosis',
                'term_ko': '진단',
                'term_zh': '诊断',
                'term_ja': '診断',
                'category': 'general',
                'description': 'Medical diagnosis'
            },
            {
                'term_en': 'treatment',
                'term_ko': '치료',
                'term_zh': '治疗',
                'term_ja': '治療',
                'category': 'general',
                'description': 'Medical treatment'
            },
            {
                'term_en': 'rhinoplasty',
                'term_ko': '코 성형',
                'term_zh': '鼻整形',
                'term_ja': '鼻形成',
                'category': 'procedure',
                'description': 'Nose reshaping surgery'
            },
            {
                'term_en': 'blepharoplasty',
                'term_ko': '눈꺼풀 성형',
                'term_zh': '眼睑整形',
                'term_ja': '眼瞼形成',
                'category': 'procedure',
                'description': 'Eyelid surgery'
            },
            {
                'term_en': 'botox',
                'term_ko': '보톡스',
                'term_zh': '肉毒杆菌',
                'term_ja': 'ボトックス',
                'category': 'treatment',
                'description': 'Botulinum toxin injection'
            },
            {
                'term_en': 'filler',
                'term_ko': '필러',
                'term_zh': '填充剂',
                'term_ja': 'フィラー',
                'category': 'treatment',
                'description': 'Dermal filler injection'
            },
            {
                'term_en': 'laser',
                'term_ko': '레이저',
                'term_zh': '激光',
                'term_ja': 'レーザー',
                'category': 'treatment',
                'description': 'Laser treatment'
            },
            {
                'term_en': 'scar',
                'term_ko': '흉터',
                'term_zh': '疤痕',
                'term_ja': '傷跡',
                'category': 'condition',
                'description': 'Scar tissue'
            },
            {
                'term_en': 'swelling',
                'term_ko': '부기',
                'term_zh': '肿胀',
                'term_ja': '腫れ',
                'category': 'symptom',
                'description': 'Post-procedure swelling'
            },
        ]

        for data in terms_data:
            term, created = MedicalTerminology.objects.get_or_create(
                term_en=data['term_en'],
                defaults=data
            )
            if created:
                self.stdout.write(f'  ✓ Created term: {term.term_en}')
            else:
                self.stdout.write(f'  - Term already exists: {term.term_en}')

        self.stdout.write(self.style.SUCCESS('\n✅ Phase 2 initialization complete!'))
        self.stdout.write(self.style.SUCCESS(f'Created:'))
        self.stdout.write(f'  - {Doctor.objects.count()} doctors')
        self.stdout.write(f'  - {DoctorAvailability.objects.count()} availability slots')
        self.stdout.write(f'  - {ProcedureType.objects.count()} procedure types')
        self.stdout.write(f'  - {MedicalTerminology.objects.count()} medical terms')