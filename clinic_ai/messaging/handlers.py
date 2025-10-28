"""
Channel-specific message handlers for multi-channel support.
Composition-based design using message handlers and processors.
"""

import json
import logging
from typing import Optional, Dict, Any
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..core.interfaces import MessageHandler, AIService, Translator, ConfigurationService
from ..core.models import Patient, Message

logger = logging.getLogger(__name__)


class KakaoHandler(MessageHandler):
    """
    KakaoTalk Business API message handler.
    Encapsulated Kakao-specific messaging logic.
    """

    def __init__(self, config_service: ConfigurationService):
        self.config = config_service
        self.api_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    def send_message(self, recipient: str, content: str, language: str = 'ko') -> bool:
        """
        Send message via KakaoTalk Business API.

        Args:
            recipient: Kakao user key (phone number)
            content: Message content
            language: Language code (for logging only)

        Returns:
            Success status
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.config.get_api_key('kakao')}",
                "Content-Type": "application/x-www-form-urlencoded"
            }

            data = {
                "template_object": json.dumps({
                    "object_type": "text",
                    "text": content,
                    "link": {
                        "web_url": "https://clinic.example.com/appointments"
                    }
                })
            }

            response = requests.post(self.api_url, headers=headers, data=data)
            response.raise_for_status()

            logger.info(f"Message sent via KakaoTalk to {recipient[:10]}...")
            return True

        except Exception as e:
            logger.error(f"KakaoTalk send error: {e}")
            return False

    def receive_message(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process incoming KakaoTalk message.

        Args:
            data: Webhook payload from Kakao

        Returns:
            Processed message data or None if invalid
        """
        try:
            user_key = data.get('user_key')
            message_text = data.get('content')

            if not user_key or not message_text:
                logger.warning("Invalid Kakao message data")
                return None

            return {
                'channel': 'kakao',
                'recipient': user_key,
                'content': message_text,
                'timestamp': data.get('timestamp'),
                'raw_data': data
            }

        except Exception as e:
            logger.error(f"Kakao message processing error: {e}")
            return None

    @property
    def channel_name(self) -> str:
        return 'kakao'


class WeChatHandler(MessageHandler):
    """
    WeChat Official Account message handler.
    Encapsulated WeChat messaging logic.
    """

    def __init__(self, config_service: ConfigurationService):
        self.config = config_service
        self.app_id = self.config.get_setting('wechat_app_id')
        self.app_secret = self.config.get_setting('wechat_app_secret')
        self.api_url = "https://api.weixin.qq.com/cgi-bin/message/custom/send"

    def send_message(self, recipient: str, content: str, language: str = 'zh') -> bool:
        """
        Send message via WeChat Official Account API.
        """
        try:
            # Get access token (simplified - would cache this in production)
            token = self._get_access_token()
            if not token:
                return False

            headers = {"Content-Type": "application/json"}
            url = f"{self.api_url}?access_token={token}"

            data = {
                "touser": recipient,
                "msgtype": "text",
                "text": {
                    "content": content
                }
            }

            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()

            result = response.json()
            if result.get('errcode') == 0:
                logger.info(f"Message sent via WeChat to {recipient}")
                return True

            logger.error(f"WeChat API error: {result}")
            return False

        except Exception as e:
            logger.error(f"WeChat send error: {e}")
            return False

    def receive_message(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process incoming WeChat message"""
        try:
            user_id = data.get('FromUserName')
            msg_type = data.get('MsgType')
            content = data.get('Content', '')

            if msg_type != 'text' or not user_id or not content:
                return None

            return {
                'channel': 'wechat',
                'recipient': user_id,
                'content': content,
                'timestamp': data.get('CreateTime'),
                'raw_data': data
            }

        except Exception as e:
            logger.error(f"WeChat message processing error: {e}")
            return None

    def _get_access_token(self) -> Optional[str]:
        """Get WeChat access token (simplified)"""
        try:
            token_url = "https://api.weixin.qq.com/cgi-bin/token"
            params = {
                'grant_type': 'client_credential',
                'appid': self.app_id,
                'secret': self.app_secret
            }

            response = requests.get(token_url, params=params)
            response.raise_for_status()

            data = response.json()
            return data.get('access_token')

        except Exception as e:
            logger.error(f"WeChat token error: {e}")
            return None

    @property
    def channel_name(self) -> str:
        return 'wechat'


class LINEHandler(MessageHandler):
    """
    LINE Official Account message handler.
    Encapsulated LINE messaging logic.
    """

    def __init__(self, config_service: ConfigurationService):
        self.config = config_service
        self.channel_access_token = self.config.get_api_key('line')
        self.api_url = "https://api.line.me/v2/bot/message/push"

    def send_message(self, recipient: str, content: str, language: str = 'ja') -> bool:
        """
        Send message via LINE Messaging API.
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.channel_access_token}",
                "Content-Type": "application/json"
            }

            data = {
                "to": recipient,
                "messages": [{
                    "type": "text",
                    "text": content
                }]
            }

            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()

            logger.info(f"Message sent via LINE to {recipient}")
            return True

        except Exception as e:
            logger.error(f"LINE send error: {e}")
            return False

    def receive_message(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process incoming LINE message"""
        try:
            events = data.get('events', [])
            if not events:
                return None

            event = events[0]  # Process first event
            user_id = event.get('source', {}).get('userId')
            msg_type = event.get('message', {}).get('type')
            content = event.get('message', {}).get('text', '')

            if msg_type != 'text' or not user_id or not content:
                return None

            return {
                'channel': 'line',
                'recipient': user_id,
                'content': content,
                'timestamp': event.get('timestamp'),
                'raw_data': data
            }

        except Exception as e:
            logger.error(f"LINE message processing error: {e}")
            return None

    @property
    def channel_name(self) -> str:
        return 'line'


class MessageProcessor:
    """
    Composite message processor using Strategy pattern.
    Composes AI service, translator, and multiple channel handlers.
    """

    def __init__(self, ai_service: AIService, translator: Translator,
                 handlers: Dict[str, MessageHandler]):
        self.ai = ai_service
        self.translator = translator
        self.handlers = handlers

    def process_message(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming message through the pipeline.

        Args:
            message_data: Message data from channel webhook

        Returns:
            Processing result with response and metadata
        """
        try:
            # 1. Validate and extract message
            channel = message_data.get('channel')
            recipient = message_data.get('recipient')
            content = message_data.get('content')

            if not all([channel, recipient, content]):
                return {'status': 'error', 'message': 'Invalid message data'}

            # 2. Get or create patient
            patient, created = Patient.objects.get_or_create(
                phone=recipient,
                defaults={
                    'name': f'Patient_{recipient[-4:]}',  # Temporary name
                    'preferred_language': self.translator.detect_language(content)
                }
            )

            # 3. Detect language and translate to Korean for processing
            detected_lang = patient.preferred_language
            korean_content = content
            if detected_lang != 'ko':
                korean_content = self.translator.translate_message(content, 'ko', detected_lang)

            # 4. Store incoming message
            incoming_msg = Message.objects.create(
                patient=patient,
                content=content,
                direction='incoming',
                channel=channel,
                confidence_score=0.8  # Initial confidence
            )

            # 5. Generate AI response
            ai_response, confidence = self.ai.generate_response(korean_content, 'ko')

            # 6. Translate response back to patient's language if needed
            final_response = ai_response
            if detected_lang != 'ko':
                final_response = self.translator.translate_message(ai_response, detected_lang, 'ko')

            # 7. Decide if AI handles or needs human
            if confidence >= 0.7:
                # AI handles - send response
                handler = self.handlers.get(channel)
                if handler:
                    success = handler.send_message(recipient, final_response, detected_lang)

                    if success:
                        # Store outgoing message
                        Message.objects.create(
                            patient=patient,
                            content=final_response,
                            direction='outgoing',
                            channel=channel,
                            is_ai_handled=True,
                            confidence_score=confidence
                        )

                        incoming_msg.is_ai_handled = True
                        incoming_msg.save()

                        return {
                            'status': 'handled',
                            'method': 'ai',
                            'confidence': confidence,
                            'language': detected_lang
                        }

            # 8. Human intervention needed
            incoming_msg.needs_human = True
            incoming_msg.save()

            # Notify staff (would implement notification service here)
            self._notify_staff(incoming_msg)

            return {
                'status': 'escalated',
                'method': 'human',
                'confidence': confidence,
                'language': detected_lang,
                'message_id': incoming_msg.id
            }

        except Exception as e:
            logger.error(f"Message processing error: {e}")
            return {'status': 'error', 'message': str(e)}

    def _notify_staff(self, message: Message) -> None:
        """Notify staff about messages needing human intervention"""
        # Would integrate with notification service
        logger.warning(f"Human intervention needed for message {message.id}: {message.content[:50]}...")

    def send_staff_response(self, message_id: int, response_text: str, staff_user) -> bool:
        """
        Send staff response through appropriate channel.
        """
        try:
            message = Message.objects.get(id=message_id)

            # Send via channel handler
            handler = self.handlers.get(message.channel)
            if not handler:
                return False

            success = handler.send_message(message.patient.phone, response_text, message.patient.preferred_language)

            if success:
                # Store staff response
                Message.objects.create(
                    patient=message.patient,
                    content=response_text,
                    direction='outgoing',
                    channel=message.channel,
                    is_ai_handled=False
                )

                message.needs_human = False
                message.save()

            return success

        except Exception as e:
            logger.error(f"Staff response error: {e}")
            return False


# Django views for webhooks
@csrf_exempt
def kakao_webhook(request):
    """KakaoTalk webhook endpoint"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'})

    try:
        data = json.loads(request.body)
        handler = KakaoHandler()  # Would inject dependencies
        processed_data = handler.receive_message(data)

        if processed_data:
            processor = MessageProcessor()  # Would inject dependencies
            result = processor.process_message(processed_data)
            return JsonResponse(result)

        return JsonResponse({'status': 'error', 'message': 'Invalid message'})

    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)})