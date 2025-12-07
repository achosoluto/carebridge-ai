from django.core.management.base import BaseCommand
from chatbot.models import KnowledgeBaseItem

class Command(BaseCommand):
    help = 'Populates the database with sample FAQ data.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating FAQ data...')

        faqs = [
            {
                'category': 'General Inquiry',
                'question': 'What are your clinic hours?',
                'answer': 'Our clinic hours are Monday to Friday from 10:00 AM to 7:00 PM, and Saturday from 10:00 AM to 5:00 PM. We are closed on Sundays and public holidays.'
            },
            {
                'category': 'General Inquiry',
                'question': 'Where is the clinic located?',
                'answer': 'We are located at 9F, KBL Center, Dosan-daero 110, Gangnam-gu, Seoul.'
            },
            {
                'category': 'Pricing',
                'question': 'How much is a consultation?',
                'answer': 'Consultation with a counselor is free. A consultation with a doctor has a fee of 20,000 KRW. This fee is waived if you proceed with a procedure on the same day or make a reservation.'
            },
            {
                'category': 'General Inquiry',
                'question': 'Do you offer translation services?',
                'answer': 'Yes, we have staff who can assist in multiple languages. Please let us know your language preference when booking your appointment.'
            },
            {
                'category': 'Pricing',
                'question': 'What is the price for Botox?',
                'answer': 'For Korean-made Botulax, the price is 99,000 KRW for the forehead or jaw. For German-made Xeomin, the price is 165,000 KRW for the forehead and 220,000 KRW for the jaw.'
            },
            {
                'category': 'Pricing',
                'question': 'What is the price for hyaluronic acid fillers?',
                'answer': 'We offer Korean-made Bellast and Chaeum fillers at 165,000 KRW per 1cc. For lips or under-eye area, the price is 220,000 KRW per 1cc.'
            },
            {
                'category': 'Procedures',
                'question': 'What should I know about nose surgery?',
                'answer': 'For nose surgery, we offer consultations to discuss the best approach for you, including non-prosthetic options. Post-surgery care involves a follow-up visit on the 2nd day for cleaning and a laser treatment to reduce swelling, and another visit after one week for stitch removal.'
            }
        ]

        for faq_data in faqs:
            KnowledgeBaseItem.objects.get_or_create(
                question=faq_data['question'],
                defaults={'answer': faq_data['answer'], 'category': faq_data['category']}
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated FAQ data.'))