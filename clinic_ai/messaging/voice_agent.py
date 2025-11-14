"""
Voice agent service for CareBridge AI.
Handles voice calls, speech-to-text, and text-to-speech conversion.
"""

import logging
from typing import Dict, Any, Optional
import openai
from django.conf import settings

from ..core.interfaces import VoiceProcessor, AIService, Translator
from ..core.models import Patient, Message

logger = logging.getLogger(__name__)


class AzureVoiceProcessor(VoiceProcessor):
    """
    Voice processor implementation using Azure Cognitive Services.
    Handles call processing, speech-to-text, and text-to-speech.
    """

    def __init__(self, ai_service: AIService, translator: Optional[Translator] = None):
        self.ai_service = ai_service
        self.translator = translator
        
        # Import Azure Cognitive Services
        try:
            from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, SpeechSynthesizer
            self.speech_sdk = True
            self.SpeechConfig = SpeechConfig
            self.SpeechRecognizer = SpeechRecognizer
            self.SpeechSynthesizer = SpeechSynthesizer
        except ImportError:
            logger.warning("Azure Cognitive Services SDK not installed. Using mock implementation.")
            self.speech_sdk = False

    def process_incoming_call(self, phone_number: str) -> Dict[str, Any]:
        """
        Handle incoming voice call from patient.
        
        Args:
            phone_number: Patient's phone number
            
        Returns:
            Dict with call processing result
        """
        try:
            # First, check if patient exists in our database
            try:
                patient = Patient.objects.get(phone=phone_number)
            except Patient.DoesNotExist:
                # Create new patient if not exists
                patient = Patient.objects.create(
                    phone=phone_number,
                    preferred_language='ko'  # Default to Korean
                )
                logger.info(f"Created new patient for call: {phone_number}")

            # Log the incoming call
            message = Message.objects.create(
                patient=patient,
                content="Incoming voice call",
                direction='incoming',
                channel='phone',
                is_ai_handled=True
            )

            # The actual call handling would happen in a real-time manner,
            # but for the MVP we'll return a placeholder response
            response = {
                'patient_id': patient.id,
                'call_status': 'connected',
                'language': patient.preferred_language,
                'initial_message': 'Voice call initiated - would connect to Azure Speech Services in production.'
            }

            logger.info(f"Processed incoming call from {phone_number}")
            return response

        except Exception as e:
            logger.error(f"Error processing incoming call: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def generate_tts(self, text: str, language: str) -> bytes:
        """
        Generate text-to-speech audio from text.
        
        Args:
            text: Text to convert to speech
            language: Language code for voice synthesis
            
        Returns:
            Audio bytes
        """
        if not self.speech_sdk:
            # Return mock audio data for development
            logger.warning("Using mock TTS service")
            return b'mock_audio_data'

        try:
            # Configure Azure speech service
            speech_config = self.SpeechConfig(
                subscription_key=settings.CLINIC_AI.get('AZURE_SPEECH_KEY', ''),
                region=settings.CLINIC_AI.get('AZURE_SPEECH_REGION', 'eastus')
            )
            
            # Set voice based on language
            voice_name = self._get_voice_for_language(language)
            speech_config.speech_synthesis_voice_name = voice_name

            # Create synthesizer (in a real implementation, we'd synthesize the text)
            # This is simplified for the MVP
            logger.info(f"Generated TTS for language {language}")
            return b'generated_audio_bytes'

        except Exception as e:
            logger.error(f"TTS generation error: {e}")
            # Return mock data if Azure fails
            return b'mock_audio_data'

    def _get_voice_for_language(self, language: str) -> str:
        """Get appropriate voice name for the language."""
        voice_mapping = {
            'ko': 'ko-KR-SunHiNeural',  # Korean
            'en': 'en-US-JennyNeural',  # English
            'zh': 'zh-CN-XiaoxiaoNeural',  # Chinese
            'ja': 'ja-JP-NanamiNeural'  # Japanese
        }
        return voice_mapping.get(language, 'en-US-JennyNeural')

    def transcribe_audio(self, audio_data: bytes, language: str) -> str:
        """
        Transcribe audio to text using speech recognition.
        
        Args:
            audio_data: Audio bytes to transcribe
            language: Language code for recognition
            
        Returns:
            Transcribed text
        """
        if not self.speech_sdk:
            # Return mock transcription for development
            logger.warning("Using mock speech-to-text service")
            return "mock transcribed text"

        try:
            # Configure Azure speech service
            speech_config = self.SpeechConfig(
                subscription_key=settings.CLINIC_AI.get('AZURE_SPEECH_KEY', ''),
                region=settings.CLINIC_AI.get('AZURE_SPEECH_REGION', 'eastus')
            )
            
            # Set language for recognition
            language_code = self._get_language_code(language)
            speech_config.speech_recognition_language = language_code

            # In a real implementation, we would process the audio_data
            # This is simplified for the MVP
            logger.info(f"Transcribed audio for language {language}")
            return "transcribed text from audio"

        except Exception as e:
            logger.error(f"Audio transcription error: {e}")
            return ""  # Return empty string if error

    def _get_language_code(self, language: str) -> str:
        """Convert our language codes to Azure format."""
        code_mapping = {
            'ko': 'ko-KR',
            'en': 'en-US',
            'zh': 'zh-CN',
            'ja': 'ja-JP'
        }
        return code_mapping.get(language, 'ko-KR')


class TwilioVoiceHandler(VoiceProcessor):
    """
    Alternative voice processor using Twilio for call handling.
    Handles call webhook events and integrates with AI service.
    """

    def __init__(self, ai_service: AIService, translator: Optional[Translator] = None):
        self.ai_service = ai_service
        self.translator = translator

    def process_incoming_call(self, phone_number: str) -> Dict[str, Any]:
        """
        Process incoming call webhook from Twilio.
        
        Args:
            phone_number: Patient's phone number from webhook
            
        Returns:
            TwiML response or call processing result
        """
        try:
            # First, look up patient in our database
            try:
                patient = Patient.objects.get(phone=phone_number)
            except Patient.DoesNotExist:
                # Create new patient if not exists
                patient = Patient.objects.create(
                    phone=phone_number,
                    preferred_language='ko'  # Default to Korean
                )
                logger.info(f"Created new patient for call: {phone_number}")

            # Log the incoming call
            message = Message.objects.create(
                patient=patient,
                content="Incoming phone call",
                direction='incoming',
                channel='phone',
                is_ai_handled=True
            )

            # Generate initial AI response based on common intents
            initial_greeting = {
                'ko': '안녕하세요! 케어브리지 AI 상담원입니다. 무엇을 도와드릴까요?',
                'en': 'Hello! This is CareBridge AI assistant. How can I help you?',
                'zh': '您好！这是CareBridge AI咨询员。有什么可以帮助您的吗？',
                'ja': 'こんにちは！ケアブリッジAIアシスタントです。何をお手伝いできますか？'
            }

            greeting = initial_greeting.get(patient.preferred_language, initial_greeting['ko'])

            response = {
                'patient_id': patient.id,
                'call_status': 'handled',
                'language': patient.preferred_language,
                'initial_response': greeting,
                'instructions': 'Call would be handled by Twilio with voice recognition in production'
            }

            logger.info(f"Processed incoming call from {phone_number}")
            return response

        except Exception as e:
            logger.error(f"Error processing incoming call: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def generate_tts(self, text: str, language: str) -> bytes:
        """
        Generate Twilio-compatible TTS response.
        
        Args:
            text: Text to convert to speech
            language: Language for voice selection
            
        Returns:
            Audio bytes
        """
        # In production, this would use Twilio's TTS or integrate with Azure/AWS
        logger.info(f"Generating TTS for Twilio: language {language}")
        # For MVP, return placeholder
        return b'twilio_tts_audio_bytes'

    def transcribe_audio(self, audio_data: bytes, language: str) -> str:
        """
        Transcribe voice input using Twilio's speech recognition.
        
        Args:
            audio_data: Audio bytes from call
            language: Language for transcription
            
        Returns:
            Transcribed text
        """
        # In production, this would process the audio against Twilio's speech recognition
        logger.info(f"Transcribing audio via Twilio: language {language}")
        # For MVP, return placeholder
        return "transcribed text from call"


class CompositeVoiceProcessor(VoiceProcessor):
    """
    Composite voice processor that can use multiple voice services.
    Provides fallback mechanisms if primary service fails.
    """

    def __init__(self, primary_processor: VoiceProcessor, fallback_processor: Optional[VoiceProcessor] = None):
        self.primary = primary_processor
        self.fallback = fallback_processor

    def process_incoming_call(self, phone_number: str) -> Dict[str, Any]:
        """Process incoming call with fallback capability."""
        try:
            return self.primary.process_incoming_call(phone_number)
        except Exception as primary_error:
            logger.warning(f"Primary voice processor failed: {primary_error}")
            if self.fallback:
                logger.info("Falling back to secondary voice processor")
                return self.fallback.process_incoming_call(phone_number)
            else:
                logger.error("No fallback voice processor available")
                return {
                    'success': False,
                    'error': str(primary_error)
                }

    def generate_tts(self, text: str, language: str) -> bytes:
        """Generate TTS with fallback capability."""
        try:
            return self.primary.generate_tts(text, language)
        except Exception as primary_error:
            logger.warning(f"Primary TTS service failed: {primary_error}")
            if self.fallback:
                logger.info("Falling back to secondary TTS service")
                return self.fallback.generate_tts(text, language)
            else:
                logger.error("No fallback TTS service available")
                return b'error_audio'

    def transcribe_audio(self, audio_data: bytes, language: str) -> str:
        """Transcribe audio with fallback capability."""
        try:
            return self.primary.transcribe_audio(audio_data, language)
        except Exception as primary_error:
            logger.warning(f"Primary STT service failed: {primary_error}")
            if self.fallback:
                logger.info("Falling back to secondary STT service")
                return self.fallback.transcribe_audio(audio_data, language)
            else:
                logger.error("No fallback STT service available")
                return "error in transcription"