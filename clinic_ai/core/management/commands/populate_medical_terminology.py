"""
Management command to populate medical terminology database with common terms.
"""

from django.core.management.base import BaseCommand
from clinic_ai.core.models import MedicalTerminology


class Command(BaseCommand):
    help = 'Populate medical terminology database with common terms'

    def handle(self, *args, **options):
        # Define medical terminology data
        medical_terms = [
            {
                'term_en': 'surgery',
                'term_ko': '수술',
                'term_zh': '手术',
                'term_ja': '手術',
                'category': 'procedure',
                'description': 'Medical procedure to treat disease or injury'
            },
            {
                'term_en': 'appointment',
                'term_ko': '예약',
                'term_zh': '预约',
                'term_ja': '予約',
                'category': 'administrative',
                'description': 'Scheduled meeting with a doctor'
            },
            {
                'term_en': 'consultation',
                'term_ko': '상담',
                'term_zh': '咨询',
                'term_ja': '相談',
                'category': 'administrative',
                'description': 'Meeting with doctor to discuss treatment'
            },
            {
                'term_en': 'injection',
                'term_ko': '주사',
                'term_zh': '注射',
                'term_ja': '注射',
                'category': 'procedure',
                'description': 'Medical procedure of introducing liquid into body'
            },
            {
                'term_en': 'filler',
                'term_ko': '필러',
                'term_zh': '填充剂',
                'term_ja': 'フィラー',
                'category': 'procedure',
                'description': 'Cosmetic injection to add volume'
            },
            {
                'term_en': 'botox',
                'term_ko': '보톡스',
                'term_zh': '肉毒素',
                'term_ja': 'ボトックス',
                'category': 'procedure',
                'description': 'Cosmetic treatment to relax muscles'
            },
            {
                'term_en': 'rhinoplasty',
                'term_ko': '코성형술',
                'term_zh': '隆鼻术',
                'term_ja': '鼻形成術',
                'category': 'procedure',
                'description': 'Surgical procedure to reshape the nose'
            },
            {
                'term_en': 'blepharoplasty',
                'term_ko': '눈성형술',
                'term_zh': '眼睑成形术',
                'term_ja': '二重瞼手術',
                'category': 'procedure',
                'description': 'Surgical procedure on the eyelids'
            },
            {
                'term_en': 'facelift',
                'term_ko': '리프팅',
                'term_zh': '面部提升',
                'term_ja': 'フェイスリフト',
                'category': 'procedure',
                'description': 'Surgical procedure to reduce signs of aging'
            },
            {
                'term_en': 'cost',
                'term_ko': '비용',
                'term_zh': '费用',
                'term_ja': '費用',
                'category': 'administrative',
                'description': 'Price or expense for treatment'
            },
            {
                'term_en': 'price',
                'term_ko': '가격',
                'term_zh': '价格',
                'term_ja': '価格',
                'category': 'administrative',
                'description': 'Amount to be paid for service'
            },
            {
                'term_en': 'location',
                'term_ko': '위치',
                'term_zh': '位置',
                'term_ja': '場所',
                'category': 'administrative',
                'description': 'Physical address or place'
            },
            {
                'term_en': 'doctor',
                'term_ko': '의사',
                'term_zh': '医生',
                'term_ja': '医師',
                'category': 'administrative',
                'description': 'Medical professional'
            },
            {
                'term_en': 'patient',
                'term_ko': '환자',
                'term_zh': '病人',
                'term_ja': '患者',
                'category': 'administrative',
                'description': 'Person receiving medical treatment'
            },
            {
                'term_en': 'medical record',
                'term_ko': '진료기록',
                'term_zh': '病历',
                'term_ja': 'カルテ',
                'category': 'administrative',
                'description': 'Documentation of patient\'s medical history'
            },
            {
                'term_en': 'anesthesia',
                'term_ko': '마취',
                'term_zh': '麻醉',
                'term_ja': '麻酔',
                'category': 'procedure',
                'description': 'Medication to prevent pain during surgery'
            },
            {
                'term_en': 'recovery',
                'term_ko': '회복',
                'term_zh': '恢复',
                'term_ja': '回復',
                'category': 'procedure',
                'description': 'Process of getting back to normal health'
            },
            {
                'term_en': 'side effect',
                'term_ko': '부작용',
                'term_zh': '副作用',
                'term_ja': '副作用',
                'category': 'procedure',
                'description': 'Unwanted effect of medical treatment'
            },
            {
                'term_en': 'swelling',
                'term_ko': '부종',
                'term_zh': '肿胀',
                'term_ja': '腫れ',
                'category': 'procedure',
                'description': 'Bulging caused by fluid accumulation'
            },
            {
                'term_en': 'consult',
                'term_ko': '상담하다',
                'term_zh': '咨询',
                'term_ja': '相談する',
                'category': 'administrative',
                'description': 'To seek advice or guidance'
            }
        ]

        created_count = 0
        updated_count = 0

        for term_data in medical_terms:
            term, created = MedicalTerminology.objects.get_or_create(
                term_en=term_data['term_en'],
                defaults={
                    'term_ko': term_data['term_ko'],
                    'term_zh': term_data['term_zh'],
                    'term_ja': term_data['term_ja'],
                    'category': term_data['category'],
                    'description': term_data['description']
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(f"Created: {term.term_en}")
            else:
                # Update existing term with new translations if they're empty
                updated = False
                if not term.term_ko and term_data['term_ko']:
                    term.term_ko = term_data['term_ko']
                    updated = True
                if not term.term_zh and term_data['term_zh']:
                    term.term_zh = term_data['term_zh']
                    updated = True
                if not term.term_ja and term_data['term_ja']:
                    term.term_ja = term_data['term_ja']
                    updated = True
                if not term.description and term_data['description']:
                    term.description = term_data['description']
                    updated = True
                if not term.category and term_data['category']:
                    term.category = term_data['category']
                    updated = True
                
                if updated:
                    term.save()
                    updated_count += 1
                    self.stdout.write(f"Updated: {term.term_en}")

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully populated medical terminology: {created_count} created, {updated_count} updated'
            )
        )