"""
Real-time translation service for multilingual patient communication.
Composition-based design with cache and fallback strategies.
"""

import requests
from typing import Optional, List
import logging

from ..core.interfaces import Translator, CacheService, ConfigurationService
from ..core.cache import SimpleCache

logger = logging.getLogger(__name__)


class GoogleTranslateService(Translator):
    """
    Google Translate API implementation.
    Single responsibility: translate text using Google Translate API.
    """

    def __init__(self, config_service: ConfigurationService, cache_service: Optional[CacheService] = None):
        self.config = config_service
        self.cache = cache_service or SimpleCache()
        self.api_key = self.config.get_api_key('google_translate')
        self.base_url = "https://translation.googleapis.com/language/translate/v2"

    def translate(self, text: str, from_lang: str, to_lang: str) -> str:
        """
        Translate text using Google Translate API with caching.

        Args:
            text: Text to translate
            from_lang: Source language code
            to_lang: Target language code

        Returns:
            Translated text
        """
        if not text.strip():
            return text

        # Create cache key
        cache_key = f"translate_{from_lang}_{to_lang}_{hash(text)}"

        # Check cache first
        cached_result = self.cache.get(cache_key)
        if cached_result:
            logger.debug(f"Translation cache hit for: {text[:50]}...")
            return cached_result

        try:
            # Make API request
            params = {
                'q': text,
                'source': from_lang,
                'target': to_lang,
                'key': self.api_key
            }

            response = requests.post(self.base_url, params=params, timeout=10)
            response.raise_for_status()

            result = response.json()
            translated_text = result['data']['translations'][0]['translatedText']

            # Cache the result for 1 hour
            self.cache.set(cache_key, translated_text, 3600)

            logger.info(f"Translation completed: {from_lang} -> {to_lang}")
            return translated_text

        except requests.RequestException as e:
            logger.error(f"Google Translate API error: {e}")
            return text  # Return original text if translation fails

    def get_supported_languages(self) -> List[str]:
        """Return list of supported language codes"""
        return [
            'af', 'sq', 'am', 'ar', 'hy', 'az', 'eu', 'be', 'bn', 'bs', 'bg', 'ca', 'ceb', 'zh', 'zh-CN', 'zh-TW',
            'co', 'hr', 'cs', 'da', 'nl', 'en', 'eo', 'et', 'fi', 'fr', 'fy', 'gl', 'ka', 'de', 'el', 'gu', 'ht',
            'ha', 'haw', 'he', 'hi', 'hmn', 'hu', 'is', 'ig', 'id', 'ga', 'it', 'ja', 'jv', 'kn', 'kk', 'km',
            'ko', 'ku', 'ky', 'lo', 'la', 'lv', 'lt', 'lb', 'mk', 'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mn',
            'my', 'ne', 'no', 'ny', 'or', 'ps', 'fa', 'pl', 'pt', 'pa', 'ro', 'ru', 'sm', 'gd', 'sr', 'st',
            'sn', 'sd', 'si', 'sk', 'sl', 'so', 'es', 'su', 'sw', 'sv', 'tl', 'tg', 'ta', 'tt', 'te', 'th',
            'tr', 'tk', 'uk', 'ur', 'ug', 'uz', 'vi', 'cy', 'xh', 'yi', 'yo', 'zu'
        ]


class SimpleLanguageDetector:
    """
    Simple language detection for MVP.
    Basic character-based detection without external dependencies.
    """

    def detect(self, text: str) -> str:
        """
        Detect language using character patterns.
        Returns language code for Korean or English.
        """
        if not text.strip():
            return 'ko'  # Default to Korean

        # Character pattern detection
        if self._has_korean_chars(text):
            return 'ko'
        elif self._is_english_text(text):
            return 'en'
        else:
            return 'ko'  # Default fallback

    def _has_korean_chars(self, text: str) -> bool:
        """Check for Korean characters"""
        return any('\uac00' <= char <= '\ud7af' for char in text)

    def _is_english_text(self, text: str) -> bool:
        """Check if text appears to be English"""
        # Simple check: ASCII proportion
        ascii_chars = sum(1 for char in text if ord(char) < 128 and char.isalnum())
        total_chars = sum(1 for char in text if char.isalnum())

        if total_chars == 0:
            return False

        return (ascii_chars / total_chars) > 0.8


class TranslationService:
    """
    Composite translation service with detection and translation.
    Uses Strategy pattern for different translation backends.
    """

    def __init__(self, translator: Translator, detector=None, cache_service: Optional[CacheService] = None):
        self.translator = translator
        self.detector = detector or SimpleLanguageDetector()
        self.cache = cache_service or SimpleCache()

    def translate_message(self, text: str, target_lang: str, source_lang: Optional[str] = None) -> str:
        """
        Translate message with automatic language detection.

        Args:
            text: Text to translate
            target_lang: Target language code
            source_lang: Optional source language (will auto-detect if not provided)

        Returns:
            Translated text
        """
        detected_lang = source_lang or self.detector.detect(text)

        # Skip translation if already in target language
        if detected_lang == target_lang:
            return text

        # Translate using configured service
        return self.translator.translate(text, detected_lang, target_lang)

    def detect_language(self, text: str) -> str:
        """Detect language of text"""
        return self.detector.detect(text)

    def is_supported_language(self, lang_code: str) -> bool:
        """Check if language is supported"""
        return lang_code in self.translator.get_supported_languages()

    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages"""
        return self.translator.get_supported_languages()

    def translate_batch(self, texts: List[str], target_lang: str) -> List[str]:
        """
        Translate multiple texts efficiently.
        Could be optimized with batch API calls in production.
        """
        return [self.translate_message(text, target_lang) for text in texts]


class FallbackTranslationService(TranslationService):
    """
    Translation service with fallback to simple dictionary translations.
    Uses Chain of Responsibility pattern.
    """

    # Simple fallback translations for common medical terms
    FALLBACK_TRANSLATIONS = {
        ('en', 'ko'): {
            'hello': '안녕하세요',
            'appointment': '예약',
            'cost': '비용',
            'location': '위치',
            'time': '시간',
            'consultation': '상담'
        },
        ('ko', 'en'): {
            '안녕하세요': 'hello',
            '예약': 'appointment',
            '비용': 'cost',
            '위치': 'location',
            '시간': 'time',
            '상담': 'consultation'
        }
    }

    def translate_message(self, text: str, target_lang: str, source_lang: Optional[str] = None) -> str:
        """
        Translate with fallback to dictionary lookup for common terms.
        """
        detected_lang = source_lang or self.detector.detect(text)

        # Try full translation first
        primary_translation = super().translate_message(text, target_lang, detected_lang)

        # If full translation failed or looks suspicious, try fallback
        if primary_translation == text or len(primary_translation.strip()) < len(text) * 0.3:
            fallback = self._get_fallback_translation(text.lower().strip(), (detected_lang, target_lang))
            if fallback:
                logger.info(f"Using fallback translation for: {text}")
                return fallback

        return primary_translation

    def _get_fallback_translation(self, text: str, lang_pair: tuple) -> Optional[str]:
        """Get fallback translation from dictionary"""
        translations = self.FALLBACK_TRANSLATIONS.get(lang_pair, {})
        return translations.get(text)