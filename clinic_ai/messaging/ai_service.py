"""
AI-powered message response service.
Composition-based design using dependency injection for translator and detector.
"""

import openai
from typing import Optional, Dict, Any, Tuple
import logging

from ..core.interfaces import AIService, Translator, LanguageDetector, ConfigurationService

logger = logging.getLogger(__name__)


class OpenAIService(AIService):
    """
    OpenAI-powered AI service implementation.
    Single responsibility: generate responses using GPT models.
    """

    def __init__(self, config_service: ConfigurationService):
        self.config = config_service
        self.client = openai.OpenAI(api_key=self.config.get_api_key('openai'))

    def generate_response(self, message: str, language: str, context: Optional[Dict] = None) -> Tuple[str, float]:
        """
        Generate AI response with confidence scoring.

        Args:
            message: User message content
            language: Detected language code
            context: Optional conversation context

        Returns:
            Tuple of (response_text, confidence_score)
        """
        try:
            system_prompts = {
                'ko': "당신은 성형외과 병원 친절한 상담 AI입니다. 간단한 질문에 답하고, 복잡한 의료상담은 반드시 '전문 상담사와 연결해드리겠습니다'라고 말하세요. 한국어로 답변합니다.",
                'en': "You are a friendly plastic surgery clinic AI assistant. Answer simple questions only. For complex medical consultations, always say 'I'll connect you with a specialist.' Respond in English.",
                'zh': "您是整形外科医院的友好咨询AI。只回答简单问题，复杂的医疗咨询请一定说'我为您转接专业咨询师'。用中文回答。",
                'ja': "美容外科医院の親切な相談AIです。簡単な質問のみ答え、複雑な医療相談は必ず「専門相談員へおつなぎします」と言ってください。日本語で回答します。"
            }

            prompt = system_prompts.get(language, system_prompts['ko'])

            # Add context if available
            if context:
                prompt += f"\nContext: {context.get('previous_intent', 'general_inquiry')}"

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=150,
                temperature=0.7
            )

            ai_response = response.choices[0].message.content.strip()
            confidence = self._calculate_confidence(ai_response, language)

            logger.info(f"AI response generated for language {language}: confidence {confidence}")
            return ai_response, confidence

        except Exception as e:
            logger.error(f"AI service error: {e}")
            fallback_responses = {
                'ko': '죄송합니다. 상담사와 연결해드리겠습니다.',
                'en': 'Sorry, let me connect you with our staff.',
                'zh': '抱歉，我为您转接咨询师。',
                'ja': '申し訳ありません。相談員にお繋ぎします。'
            }
            return fallback_responses.get(language, fallback_responses['ko']), 0.0

    def classify_intent(self, message: str) -> Dict[str, Any]:
        """
        Classify user intent with confidence scoring.

        Returns:
            Dict containing intent, confidence, and entities
        """
        intents = {
            'appointment': ['예약', 'appointment', '预约', '予約', 'schedule'],
            'pricing': ['비용', '가격', 'price', 'cost', '费用', '料金'],
            'location': ['위치', '주소', 'location', 'address', '位置', '場所'],
            'procedure': ['수술', '시술', 'surgery', 'procedure', '手术', '手術'],
            'consultation': ['상담', 'consultation', '咨询', '相談']
        }

        message_lower = message.lower()
        scores = {}

        for intent, keywords in intents.items():
            score = sum(1 for keyword in keywords if keyword.lower() in message_lower)
            if score > 0:
                scores[intent] = score

        if scores:
            best_intent = max(scores, key=scores.get)
            confidence = min(scores[best_intent] / 2.0, 1.0)  # Normalize to 0-1
            return {
                'intent': best_intent,
                'confidence': confidence,
                'scores': scores
            }

        return {
            'intent': 'general',
            'confidence': 0.1,
            'scores': {}
        }

    def _calculate_confidence(self, response: str, language: str) -> float:
        """
        Calculate confidence score based on response characteristics.
        """
        uncertainty_phrases = {
            'ko': ['모르겠', '확실하지', '상담사', '전문가', '알려주'],
            'en': ["don't know", "not sure", "specialist", "doctor", "let me"],
            'zh': ['不知道', '不确定', '咨询师', '医生', '我来'],
            'ja': ['分かりません', '専門家', '相談員', 'お手伝い']
        }

        phrases = uncertainty_phrases.get(language, uncertainty_phrases['ko'])

        if any(phrase in response.lower() for phrase in phrases):
            return 0.3  # Low confidence - suggests human handoff

        # High confidence for direct, informative responses
        if len(response) > 50 and any(word in response.lower() for word in ['있습니다', '합니다', 'available', '가능', '是的', 'できます']):
            return 0.9

        return 0.7  # Medium confidence default


class KeywordBasedAIService(AIService):
    """
    Simple keyword-based AI service for basic responses.
    Fallback when OpenAI is unavailable.
    """

    QUICK_RESPONSES = {
        'ko': {
            '가격': '수술 비용은 상담 후 결정됩니다. 예약하시겠어요?',
            '비용': '정확한 비용은 상담 후 안내드립니다.',
            '예약': '예약을 도와드리겠습니다. 언제 방문 가능하신가요?',
            '위치': '저희 병원은 강남구 논현로 123번지에 있습니다.',
            '시간': '진료시간: 평일 9-18시, 토요일 9-13시',
            '주차': '지하 주차장을 이용해주세요.',
        },
        'en': {
            'price': 'Costs are determined after consultation. Would you like to book?',
            'cost': 'Exact costs provided after consultation.',
            'appointment': 'I can help with booking. When are you available?',
            'location': 'Our clinic is at 123 Nonhyeon-ro, Gangnam-gu.',
            'time': 'Hours: Mon-Fri 9-18, Sat 9-13',
            'parking': 'Please use underground parking.',
        },
        'zh': {
            'price': '手术费用需要咨询后确定。需要预约吗？',
            'cost': '具体费用咨询后告知。',
            'appointment': '我来帮您预约。您什么时候方便？',
            'location': '我们医院位于江南区论岘路123号。',
            'time': '诊疗时间：周一至五9-18点，周六9-13点',
            'parking': '请使用地下停车场。',
        },
        'ja': {
            'price': '手術費用はカウンセリング後決定します。予約されますか？',
            'cost': '正確な費用はカウンセリング後お知らせします。',
            'appointment': '予約をお手伝いします。いつご都合がよろしいですか？',
            'location': '病院は江南区論峴路123番地にあります。',
            'time': '診療時間：平日9-18時、土曜日9-13時',
            'parking': '地下駐車場をご利用ください。',
        }
    }

    def generate_response(self, message: str, language: str, context: Optional[Dict] = None) -> Tuple[str, float]:
        """Generate keyword-based response"""
        message_lower = message.lower()
        responses = self.QUICK_RESPONSES.get(language, self.QUICK_RESPONSES['ko'])

        for keyword, response in responses.items():
            if keyword in message_lower:
                return response, 0.8  # Good confidence for keyword matches

        # Default response if no keywords match
        default_responses = {
            'ko': '안녕하세요! 어떤 도움이 필요하신가요?',
            'en': 'Hello! How can I help you today?',
            'zh': '您好！我可以怎么帮助您？',
            'ja': 'こんにちは！どうお手伝いできますか？'
        }
        return default_responses.get(language, default_responses['ko']), 0.6

    def classify_intent(self, message: str) -> Dict[str, Any]:
        """Simple keyword-based intent classification"""
        return {
            'intent': 'general',
            'confidence': 0.5,
            'method': 'keyword'
        }


class CompositeAIService(AIService):
    """
    Composite AI service that combines multiple response strategies.
    Uses Strategy pattern for response generation.
    """

    def __init__(self, primary_service: AIService, fallback_service: AIService,
                 translator: Optional[Translator] = None):
        self.primary = primary_service
        self.fallback = fallback_service
        self.translator = translator

    def generate_response(self, message: str, language: str, context: Optional[Dict] = None) -> Tuple[str, float]:
        """
        Try primary service, fallback to secondary if confidence is low.
        """
        primary_response, primary_confidence = self.primary.generate_response(message, language, context)

        if primary_confidence >= 0.7:
            return primary_response, primary_confidence

        # Use fallback service
        logger.info(f"Using fallback AI service for message: {message[:50]}...")
        return self.fallback.generate_response(message, language, context)

    def classify_intent(self, message: str) -> Dict[str, Any]:
        """Combine intent classification from both services"""
        primary_intent = self.primary.classify_intent(message)
        fallback_intent = self.fallback.classify_intent(message)

        # Return the more confident classification
        return primary_intent if primary_intent['confidence'] > fallback_intent['confidence'] else fallback_intent