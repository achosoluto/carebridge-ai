"""Management command to load realistic customer conversation data."""

from django.core.management.base import BaseCommand
from clinic_ai.core.models import Patient, Message
from django.utils import timezone
from datetime import timedelta
import random


class Command(BaseCommand):
    help = 'Load realistic customer conversations for plastic surgery clinic'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Loading realistic customer conversations...')
        )
        
        # Create Korean customer conversation
        self.create_korean_conversation()
        
        # Create Japanese customer conversation (from real data)
        self.create_japanese_conversation()
        
        # Create Chinese customer conversation (from real data)
        self.create_chinese_conversation()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully loaded all customer conversations!')
        )

    def create_korean_conversation(self):
        """Create realistic Korean customer conversation for plastic surgery."""
        
        # Create Korean patient
        patient, _ = Patient.objects.get_or_create(
            phone='+821087654321',
            defaults={
                'name': '박지은',
                'preferred_language': 'ko'
            }
        )
        
        # Conversation flow: Initial inquiry -> Consultation booking -> Price inquiry -> Confirmation
        conversations = [
            # Day 1: Initial contact
            {
                'content': '안녕하세요, 쌍꺼풀 수술 상담 받고 싶은데 가능한가요?',
                'direction': 'incoming',
                'time_offset': -7,  # 7 days ago
                'is_ai': False,
                'needs_human': True,
                'confidence': 0.85
            },
            {
                'content': '안녕하세요! 치유성형외과입니다. 쌍꺼풀 상담 도와드리겠습니다. 😊\n\n상담 예약을 위해 다음 정보를 알려주세요:\n1. 성함 / 나이\n2. 연락처\n3. 희망 상담 날짜 (2-3개 후보)\n4. 수술 경험 유무\n\n상담 시간은 약 1-2시간 소요되며, 원장님 상담료는 1-2만원입니다.',
                'direction': 'outgoing',
                'time_offset': -7,
                'is_ai': True,
                'needs_human': False,
                'confidence': 0.92
            },
            {
                'content': '1. 박지은 / 28세\n2. 010-8765-4321\n3. 이번주 금요일 오후나 다음주 월요일 오전\n4. 수술 경험 없습니다',
                'direction': 'incoming',
                'time_offset': -7,
                'is_ai': False,
                'needs_human': False,
                'confidence': 0.88
            },
            {
                'content': '감사합니다! 다음주 월요일 오전 10시 가능하신가요?\n\n쌍꺼풀 수술의 경우:\n- 매몰법: 120-150만원\n- 절개법: 180-220만원\n- 눈매교정 포함시 추가 50-80만원\n\n정확한 비용은 상담 후 결정됩니다.',
                'direction': 'outgoing',
                'time_offset': -7,
                'is_ai': True,
                'needs_human': False,
                'confidence': 0.90
            },
            {
                'content': '네, 월요일 10시 좋습니다. 매몰법과 절개법 차이도 상담때 여쭤볼게요!',
                'direction': 'incoming',
                'time_offset': -7,
                'is_ai': False,
                'needs_human': False,
                'confidence': 0.95
            },
            {
                'content': '예약 완료되었습니다! ✅\n\n📅 상담 일시: 11월 25일 (월) 오전 10:00\n👤 성함: 박지은님\n📍 위치: 서울시 강남구 도산대로 110, KBL센터 9층\n\n상담 당일 신분증 지참 부탁드립니다.\n전날 확인 문자 드리겠습니다! 😊',
                'direction': 'outgoing',
                'time_offset': -7,
                'is_ai': True,
                'needs_human': False,
                'confidence': 0.93
            },
            # Day 6: Pre-appointment reminder
            {
                'content': '안녕하세요 박지은님! 😊\n내일 오전 10시 쌍꺼풀 상담 예약 확인차 연락드립니다.\n\n예정대로 방문 가능하신가요?',
                'direction': 'outgoing',
                'time_offset': -1,
                'is_ai': True,
                'needs_human': False,
                'confidence': 0.91
            },
            {
                'content': '네, 내일 10시에 방문하겠습니다!',
                'direction': 'incoming',
                'time_offset': -1,
                'is_ai': False,
                'needs_human': False,
                'confidence': 0.96
            },
            # Day 7: Post-consultation
            {
                'content': '오늘 상담 감사했습니다! 😊\n\n상담 내용 정리:\n✅ 권장 시술: 매몰법 + 눈매교정\n✅ 예상 비용: 200만원\n✅ 회복 기간: 1주일 (실밥 제거)\n✅ 수술 예약: 12월 5일 오전 9시\n\n수술 전 주의사항은 문자로 발송해드렸습니다.',
                'direction': 'outgoing',
                'time_offset': 0,
                'is_ai': False,
                'needs_human': True,
                'confidence': 0.88
            },
            {
                'content': '네, 감사합니다! 12월 5일에 뵙겠습니다 :)',
                'direction': 'incoming',
                'time_offset': 0,
                'is_ai': False,
                'needs_human': False,
                'confidence': 0.94
            }
        ]
        
        base_time = timezone.now()
        for conv in conversations:
            Message.objects.create(
                patient=patient,
                content=conv['content'],
                direction=conv['direction'],
                channel='kakao',
                is_ai_handled=conv['is_ai'],
                needs_human=conv['needs_human'],
                confidence_score=conv['confidence'],
                created_at=base_time + timedelta(days=conv['time_offset'])
            )
        
        self.stdout.write(f'Created Korean conversation for {patient.name}')

    def create_japanese_conversation(self):
        """Create Japanese customer conversation based on real data."""
        
        patient, _ = Patient.objects.get_or_create(
            phone='+819012345678',
            defaults={
                'name': '中村さくら',
                'preferred_language': 'ja'
            }
        )
        
        conversations = [
            {
                'content': 'はじめまして。鼻のカウンセリングを検討しております。11月5日16:00以降で空いている時間はありますでしょうか?',
                'direction': 'incoming',
                'time_offset': -10,
                'is_ai': False,
                'needs_human': True,
                'confidence': 0.82
            },
            {
                'content': 'お世話になっております。\n\n1. 手術予定日はいつでしょうか？\n2. ご希望の担当ドクターはいらっしゃいますか？\n3. 初めて手術か、またはフィラー施術のご経験があるかをお知らせいただけますでしょうか。\n4. 当院をどのようにお知りになりましたか？\n\nカウンセリング所要時間は約2時間かかります❣\n院長のカウンセリング費は1〜2万ウォン、CT撮影は2万ウォンとなります。',
                'direction': 'outgoing',
                'time_offset': -10,
                'is_ai': True,
                'needs_human': False,
                'confidence': 0.89
            },
            {
                'content': '1.年内\n2.チョンナムジュ院長\n3.唇フィラー等あり(手術はありません)\n4.Twitter\nよろしくお願いいたします。',
                'direction': 'incoming',
                'time_offset': -10,
                'is_ai': False,
                'needs_human': False,
                'confidence': 0.91
            },
            {
                'content': '11月5日17:00はいかがでしょうか🙏\n\n👩‍💬 オンラインカウンセリングは日本語で対応可能です。\nご来院の際は、通訳の方にご同伴いただくとスムーズにご案内できますのでご参考ください。\nもし通訳のご準備が難しい場合は、事前にお知らせくださいませ。🌿',
                'direction': 'outgoing',
                'time_offset': -10,
                'is_ai': True,
                'needs_human': False,
                'confidence': 0.87
            },
            {
                'content': '11月5日17:00でよろしくお願いいたします。通訳者を連れていくことが難しいのですが大丈夫でしょうか?',
                'direction': 'incoming',
                'time_offset': -10,
                'is_ai': False,
                'needs_human': True,
                'confidence': 0.84
            },
            {
                'content': '大丈夫ですよ😊\n以下の情報をご記入いただくと、予約が完了いたします。\n\n1. 氏名 ＋ パスポート記載の英語氏名：\n\n* 韓国の病院では現在、実名制予約を実施しておりますので、有効な身分証（パスポートまたは外国人登録証）を必ずご持参ください。',
                'direction': 'outgoing',
                'time_offset': -10,
                'is_ai': False,
                'needs_human': True,
                'confidence': 0.90
            },
            {
                'content': '中村さくら / NAKAMURA SAKURA\n当日はどうぞよろしくお願いいたします。',
                'direction': 'incoming',
                'time_offset': -10,
                'is_ai': False,
                'needs_human': False,
                'confidence': 0.93
            },
            {
                'content': 'どうぞよろしくお願いいたします😊',
                'direction': 'outgoing',
                'time_offset': -10,
                'is_ai': True,
                'needs_human': False,
                'confidence': 0.95
            },
            {
                'content': 'お世話になっております。11月5日17:00予約させていただいているのですが、14:00頃に変更は可能でしょうか?',
                'direction': 'incoming',
                'time_offset': -3,
                'is_ai': False,
                'needs_human': True,
                'confidence': 0.86
            },
            {
                'content': 'お世話になっております🙏 14:00に変更致しました！どうぞよろしくお願いいたします。',
                'direction': 'outgoing',
                'time_offset': -3,
                'is_ai': False,
                'needs_human': True,
                'confidence': 0.92
            },
            {
                'content': '本日は、当院へご来院いただき、誠にありがとうございました。\n\n🩺 施術内容（ご提案の要点）\n手術方法： 無プロテーゼ\nデザイン： 鼻先を少しシャープに整え、角度も少し上げる\n\n📅 術後のスケジュールとケア\n術後2日目： 鼻内の綿球除去、消毒\n術後1週間目： 抜糸、角質ケアサービス',
                'direction': 'outgoing',
                'time_offset': 0,
                'is_ai': False,
                'needs_human': True,
                'confidence': 0.88
            }
        ]
        
        base_time = timezone.now()
        for conv in conversations:
            Message.objects.create(
                patient=patient,
                content=conv['content'],
                direction=conv['direction'],
                channel='line',
                is_ai_handled=conv['is_ai'],
                needs_human=conv['needs_human'],
                confidence_score=conv['confidence'],
                created_at=base_time + timedelta(days=conv['time_offset'])
            )
        
        self.stdout.write(f'Created Japanese conversation for {patient.name}')

    def create_chinese_conversation(self):
        """Create Chinese customer conversation based on real data."""
        
        patient, _ = Patient.objects.get_or_create(
            phone='+886912345678',
            defaults={
                'name': '黃嘉怡',
                'preferred_language': 'zh'
            }
        )
        
        conversations = [
            {
                'content': '您好 想請問咀嚼肌肉毒、嘴唇玻尿酸、美版超聲刀的價錢，謝謝🙏',
                'direction': 'incoming',
                'time_offset': -15,
                'is_ai': False,
                'needs_human': True,
                'confidence': 0.83
            },
            {
                'content': '您好🥰項目價格可以參考目前的活動：\n\n▶肉毒素\n[ 韓國產 Botulax ]\n- 額頭 9.9萬韓幣\n- 咀嚼肌 9.9萬韓幣\n\n[ 德國產 西馬 Xeomin ]\n- 額頭 16.5萬韓幣\n- 咀嚼肌 22萬韓幣\n\n▶玻尿酸/填充劑\n韓國產 貝拉斯特 1cc/16.5萬韓幣\n- 嘴巴/臥蠶 1cc/22萬韓幣',
                'direction': 'outgoing',
                'time_offset': -15,
                'is_ai': True,
                'needs_human': False,
                'confidence': 0.91
            },
            {
                'content': '好的謝謝，請問有美版音波嗎🤩',
                'direction': 'incoming',
                'time_offset': -15,
                'is_ai': False,
                'needs_human': True,
                'confidence': 0.85
            },
            {
                'content': '目前美版音波還在準備中',
                'direction': 'outgoing',
                'time_offset': -15,
                'is_ai': True,
                'needs_human': False,
                'confidence': 0.94
            },
            {
                'content': '了解😊 請問諮詢的話是諮詢師看完後院長會再評估一次嗎？中文服務都會陪同整個過程嗎🥹 謝謝🙏',
                'direction': 'incoming',
                'time_offset': -15,
                'is_ai': False,
                'needs_human': True,
                'confidence': 0.80
            },
            {
                'content': '對的哦\n諮詢師會先了解您的需求，然後院長會親自評估。\n中文服務會全程陪同，請放心😊',
                'direction': 'outgoing',
                'time_offset': -15,
                'is_ai': False,
                'needs_human': True,
                'confidence': 0.89
            },
            {
                'content': '好的😆 我想預約3/7 早上10:30  3位 謝謝🙏',
                'direction': 'incoming',
                'time_offset': -14,
                'is_ai': False,
                'needs_human': True,
                'confidence': 0.87
            },
            {
                'content': '3/7 目前都滿囉',
                'direction': 'outgoing',
                'time_offset': -14,
                'is_ai': True,
                'needs_human': False,
                'confidence': 0.92
            },
            {
                'content': '那請問3/6呢🥹',
                'direction': 'incoming',
                'time_offset': -14,
                'is_ai': False,
                'needs_human': False,
                'confidence': 0.88
            },
            {
                'content': '3/6 10點兩位 11:30一位 這樣可以\n請填寫以下資訊，完成您的預約😊\n\n1. 中文名+護照上英文名：\n2. 西元出生年月日+性別：\n3. 國籍/常住國家：\n4. 近3個月內醫美or手術內容：\n5. 諮詢&施作項目：\n6. 是否希望當天諮詢後施作（是/否/未定）：',
                'direction': 'outgoing',
                'time_offset': -14,
                'is_ai': True,
                'needs_human': False,
                'confidence': 0.90
            },
            {
                'content': '1. 黃嘉怡 Huang Jiayi\n2. 1995/03/15 女\n3. 台灣\n4. 無\n5. 電音波/咀嚼肌肉毒/嘴唇\n6. 是',
                'direction': 'incoming',
                'time_offset': -14,
                'is_ai': False,
                'needs_human': False,
                'confidence': 0.93
            },
            {
                'content': '您已預約成功✅\n\n(*)預約時間(*)\n3月6日, 星期四, 上午 10:00\n預約人數 : 1位\n\n(*)本院地址(*)\n首爾市 江南區 島山大路110, KBL中心 9樓',
                'direction': 'outgoing',
                'time_offset': -14,
                'is_ai': True,
                'needs_human': False,
                'confidence': 0.91
            },
            {
                'content': '收到～謝謝您',
                'direction': 'incoming',
                'time_offset': -14,
                'is_ai': False,
                'needs_human': False,
                'confidence': 0.95
            },
            {
                'content': '您好😊 請務必回覆此條內容！\n您的面診(*)預約時間(*)\n3月6日, 星期四, 上午 10:00\n預約人數 : 1位\n───────────────\n請問可以準時過來嗎？如果行程沒有變動，請務必回覆喔‼',
                'direction': 'outgoing',
                'time_offset': -1,
                'is_ai': True,
                'needs_human': False,
                'confidence': 0.90
            },
            {
                'content': '會準時過去喔！謝謝',
                'direction': 'incoming',
                'time_offset': -1,
                'is_ai': False,
                'needs_human': False,
                'confidence': 0.96
            },
            {
                'content': '您好！今天施作項目的[施術後注意事項]\n\n▶ 除皺針/肌肉肉毒\n1. 建議療程後的7天內避免使用三溫暖或汗蒸房。\n2. 咀嚼肌：像魷魚這類較硬或有嚼勁的食物應盡量避免食用。\n3. 效果：肌肉的肉毒桿菌需3週後見效。\n\n▶ 玻尿酸/填充劑\n1. 施術部位可能會有輕微泛紅，通常在1~2天內會消退。\n2. 施術後的2~3天內，請儘量避免飲酒、吸煙。',
                'direction': 'outgoing',
                'time_offset': 0,
                'is_ai': False,
                'needs_human': True,
                'confidence': 0.87
            }
        ]
        
        base_time = timezone.now()
        for conv in conversations:
            Message.objects.create(
                patient=patient,
                content=conv['content'],
                direction=conv['direction'],
                channel='wechat',
                is_ai_handled=conv['is_ai'],
                needs_human=conv['needs_human'],
                confidence_score=conv['confidence'],
                created_at=base_time + timedelta(days=conv['time_offset'])
            )
        
        self.stdout.write(f'Created Chinese conversation for {patient.name}')
