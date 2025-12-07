from django.conf import settings
from django.utils.module_loading import import_string
try:
    from google.cloud import translate_v2 as translate
except ImportError:
    translate = None
import os
import logging

logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self):
        self.client = None
        
        # Dynamically load the translation client
        if hasattr(settings, 'TRANSLATION_SERVICE_CLASS'):
            try:
                client_class = import_string(settings.TRANSLATION_SERVICE_CLASS)
                self.client = client_class()
                logger.info(f"Translation client {settings.TRANSLATION_SERVICE_CLASS} initialized.")
                return
            except (ImportError, AttributeError) as e:
                logger.warning(f"Failed to load translation client class: {e}")

        # Fallback to default Google Translate client
        if os.getenv("GOOGLE_APPLICATION_CREDENTIALS") or os.getenv("GOOGLE_API_KEY"):
            try:
                self.client = translate.Client()
                logger.info("Google Translate Client initialized.")
            except Exception as e:
                logger.warning(f"Failed to initialize Google Translate Client: {e}")
        else:
            logger.info("No Google Credentials found. Using Mock Translation Service.")

    def translate_text(self, text, target_language, source_language=None):
        """
        Translates text to the target language.
        Args:
            text (str): The text to translate.
            target_language (str): The target language code (e.g., 'en', 'ja', 'zh').
            source_language (str): The source language code (optional).
        Returns:
            str: The translated text.
        """
        if not text:
            return ""

        if self.client:
            try:
                # Google Translate API call
                result = self.client.translate(
                    text, 
                    target_language=target_language, 
                    source_language=source_language
                )
                return result['translatedText']
            except Exception as e:
                logger.error(f"Translation API error: {e}")
                return f"[Error: {text}]"
        else:
            # Mock translation for development
            return f"[{target_language.upper()}] {text}"

# Singleton instance
translation_service = TranslationService()
