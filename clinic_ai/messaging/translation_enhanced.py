"""
Enhanced translation service for Phase 2 with Google Translate API integration.
Includes medical terminology support, translation history, and quality tracking.
"""

import requests
import time
from typing import Optional, List, Dict, Any, Tuple
import logging
from django.core.cache import cache
from django.db import transaction

from ..core.interfaces import Translator, CacheService, ConfigurationService
from ..core.models import TranslationHistory, MedicalTerminology
from .translation import SimpleLanguageDetector

logger = logging.getLogger(__name__)


class EnhancedGoogleTranslateService(Translator):
    """
    Enhanced Google Translate API implementation with medical terminology support.
    Tracks translation history and quality metrics.
    """

    def __init__(self, config_service: ConfigurationService, cache_service: Optional[CacheService] = None):
        self.config = config_service
        self.cache = cache_service
        self.api_key = self.config.get_api_key('google_translate')
        self.base_url = "https://translation.googleapis.com/language/translate/v2"
        self.medical_terms_cache = {}
        self._load_medical_terminology()

    def _load_medical_terminology(self):
        """Load medical terminology into memory cache for fast lookup."""
        try:
            terms = MedicalTerminology.objects.all()
            for term in terms:
                # Create lookup dictionary for each language
                self.medical_terms_cache[term.term_en.lower()] = {
                    'ko': term.term_ko,
                    'zh': term.term_zh,
                    'ja': term.term_ja,
                    'en': term.term_en,
                    'category': term.category
                }
            logger.info(f"Loaded {len(self.medical_terms_cache)} medical terms into cache")
        except Exception as e:
            logger.warning(f"Could not load medical terminology: {e}")

    def translate(self, text: str, from_lang: str, to_lang: str, 
                  message_id: Optional[int] = None,
                  track_history: bool = True) -> str:
        """
        Translate text using Google Translate API with medical terminology enhancement.

        Args:
            text: Text to translate
            from_lang: Source language code
            to_lang: Target language code
            message_id: Optional message ID for history tracking
            track_history: Whether to save translation history

        Returns:
            Translated text
        """
        if not text.strip():
            return text

        start_time = time.time()
        
        # Check cache first
        cache_key = f"translate_v2_{from_lang}_{to_lang}_{hash(text)}"
        cached_result = cache.get(cache_key) if self.cache else None
        
        if cached_result:
            logger.debug(f"Translation cache hit for: {text[:50]}...")
            return cached_result

        try:
            # Pre-process medical terminology
            processed_text, medical_terms_found = self._preprocess_medical_terms(text, from_lang)
            
            # Make API request
            params = {
                'q': processed_text,
                'source': from_lang,
                'target': to_lang,
                'key': self.api_key,
                'format': 'text'
            }

            response = requests.post(self.base_url, params=params, timeout=10)
            response.raise_for_status()

            result = response.json()
            translated_text = result['data']['translations'][0]['translatedText']
            
            # Post-process medical terminology
            translated_text = self._postprocess_medical_terms(
                translated_text, medical_terms_found, to_lang
            )

            # Calculate processing time
            processing_time_ms = int((time.time() - start_time) * 1000)

            # Cache the result for 1 hour
            if self.cache:
                cache.set(cache_key, translated_text, 3600)

            # Track translation history
            if track_history:
                self._save_translation_history(
                    source_text=text,
                    translated_text=translated_text,
                    source_language=from_lang,
                    target_language=to_lang,
                    message_id=message_id,
                    is_medical=len(medical_terms_found) > 0,
                    processing_time_ms=processing_time_ms
                )

            logger.info(f"Translation completed: {from_lang} -> {to_lang} ({processing_time_ms}ms)")
            return translated_text

        except requests.RequestException as e:
            logger.error(f"Google Translate API error: {e}")
            # Save failed translation attempt
            if track_history:
                self._save_translation_history(
                    source_text=text,
                    translated_text=text,
                    source_language=from_lang,
                    target_language=to_lang,
                    message_id=message_id,
                    confidence_score=0.0
                )
            return text  # Return original text if translation fails

    def _preprocess_medical_terms(self, text: str, source_lang: str) -> Tuple[str, List[Dict]]:
        """
        Identify and mark medical terms in text for accurate translation.
        
        Returns:
            Tuple of (processed_text, list of found medical terms)
        """
        medical_terms_found = []
        processed_text = text
        
        # Check for medical terms in the text
        words = text.lower().split()
        for word in words:
            if word in self.medical_terms_cache:
                term_info = self.medical_terms_cache[word]
                medical_terms_found.append({
                    'original': word,
                    'info': term_info
                })
                # Update usage count
                try:
                    MedicalTerminology.objects.filter(term_en__iexact=word).update(
                        usage_count=models.F('usage_count') + 1
                    )
                except Exception as e:
                    logger.warning(f"Could not update medical term usage: {e}")
        
        return processed_text, medical_terms_found

    def _postprocess_medical_terms(self, translated_text: str, 
                                   medical_terms: List[Dict], 
                                   target_lang: str) -> str:
        """
        Replace translated medical terms with accurate terminology.
        """
        result = translated_text
        
        for term_data in medical_terms:
            term_info = term_data['info']
            accurate_translation = term_info.get(target_lang)
            
            if accurate_translation:
                # This is a simple replacement - in production, use more sophisticated NLP
                result = result.replace(
                    term_data['original'], 
                    accurate_translation
                )
        
        return result

    def _save_translation_history(self, source_text: str, translated_text: str,
                                 source_language: str, target_language: str,
                                 message_id: Optional[int] = None,
                                 is_medical: bool = False,
                                 processing_time_ms: Optional[int] = None,
                                 confidence_score: Optional[float] = None):
        """Save translation to history for audit and quality tracking."""
        try:
            from ..core.models import Message
            
            message = None
            if message_id:
                try:
                    message = Message.objects.get(id=message_id)
                except Message.DoesNotExist:
                    pass

            TranslationHistory.objects.create(
                message=message,
                source_text=source_text[:1000],  # Limit length
                translated_text=translated_text[:1000],
                source_language=source_language,
                target_language=target_language,
                translation_service='google',
                confidence_score=confidence_score or 0.95,
                is_medical_terminology=is_medical,
                processing_time_ms=processing_time_ms
            )
        except Exception as e:
            logger.error(f"Failed to save translation history: {e}")

    def get_supported_languages(self) -> List[str]:
        """Return list of supported language codes (Korean, English for MVP)"""
        return ['ko', 'en']

    def batch_translate(self, texts: List[str], from_lang: str, to_lang: str) -> List[str]:
        """
        Translate multiple texts efficiently using batch API.
        """
        if not texts:
            return []

        try:
            # Google Translate API supports batch translation
            params = {
                'q': texts,
                'source': from_lang,
                'target': to_lang,
                'key': self.api_key,
                'format': 'text'
            }

            response = requests.post(self.base_url, params=params, timeout=30)
            response.raise_for_status()

            result = response.json()
            translations = [t['translatedText'] for t in result['data']['translations']]
            
            logger.info(f"Batch translated {len(texts)} texts: {from_lang} -> {to_lang}")
            return translations

        except requests.RequestException as e:
            logger.error(f"Batch translation error: {e}")
            return texts  # Return original texts if translation fails


class EnhancedTranslationService:
    """
    Enhanced translation service with quality tracking and medical terminology.
    Wrapper around EnhancedGoogleTranslateService with additional features.
    """

    def __init__(self, translator: Translator, detector=None, cache_service: Optional[CacheService] = None):
        self.translator = translator
        self.detector = detector or SimpleLanguageDetector()
        self.cache = cache_service

    def translate_message(self, text: str, target_lang: str, 
                         source_lang: Optional[str] = None,
                         message_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Translate message with automatic language detection and quality tracking.

        Returns:
            Dict containing translated text and metadata
        """
        detected_lang = source_lang or self.detector.detect(text)

        # Skip translation if already in target language
        if detected_lang == target_lang:
            return {
                'translated_text': text,
                'source_language': detected_lang,
                'target_language': target_lang,
                'skipped': True
            }

        # Translate using configured service
        start_time = time.time()
        # Check if the translator supports the message_id parameter
        if hasattr(self.translator, '_save_translation_history'):
            # EnhancedGoogleTranslateService with message_id support
            translated_text = self.translator.translate(
                text, detected_lang, target_lang, message_id=message_id
            )
        else:
            # Standard translator interface
            translated_text = self.translator.translate(text, detected_lang, target_lang)
        processing_time = time.time() - start_time

        return {
            'translated_text': translated_text,
            'source_language': detected_lang,
            'target_language': target_lang,
            'processing_time_ms': int(processing_time * 1000),
            'skipped': False
        }

    def detect_language(self, text: str) -> str:
        """Detect language of text"""
        return self.detector.detect(text)

    def get_translation_quality_score(self, translation_id: int) -> Optional[float]:
        """Get quality score for a specific translation."""
        try:
            translation = TranslationHistory.objects.get(id=translation_id)
            return translation.quality_score
        except TranslationHistory.DoesNotExist:
            return None

    def update_translation_quality(self, translation_id: int, quality_score: float) -> bool:
        """Update quality score for a translation (manual feedback)."""
        try:
            translation = TranslationHistory.objects.get(id=translation_id)
            translation.quality_score = quality_score
            translation.save()
            logger.info(f"Updated translation quality score: {translation_id} -> {quality_score}")
            return True
        except TranslationHistory.DoesNotExist:
            return False

    def get_translation_stats(self, days: int = 30) -> Dict[str, Any]:
        """Get translation statistics for the specified period."""
        from django.utils import timezone
        from datetime import timedelta
        
        cutoff_date = timezone.now() - timedelta(days=days)
        
        translations = TranslationHistory.objects.filter(created_at__gte=cutoff_date)
        
        total_count = translations.count()
        medical_count = translations.filter(is_medical_terminology=True).count()
        avg_processing_time = translations.aggregate(
            avg_time=models.Avg('processing_time_ms')
        )['avg_time'] or 0
        
        avg_quality = translations.filter(
            quality_score__isnull=False
        ).aggregate(
            avg_quality=models.Avg('quality_score')
        )['avg_quality'] or 0

        return {
            'total_translations': total_count,
            'medical_translations': medical_count,
            'average_processing_time_ms': round(avg_processing_time, 2),
            'average_quality_score': round(avg_quality, 2),
            'period_days': days
        }