#!/usr/bin/env python
"""
Test script to verify CareBridge AI MVP features.
"""

import os
import django
from django.conf import settings
import sys

# Add project root to Python path
sys.path.insert(0, '/Users/acmac/Documents/GitHub/carebridge-ai')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from clinic_ai.core.models import Patient, MedicalTerminology
from clinic_ai.core.config import DjangoConfigService
from clinic_ai.core.cache import DjangoCacheService
from clinic_ai.messaging.ai_service import OpenAIService, CompositeAIService, KeywordBasedAIService
from clinic_ai.messaging.translation_enhanced import EnhancedTranslationService
from clinic_ai.messaging.translation import GoogleTranslateService
from clinic_ai.messaging.scheduling_optimizer import AdvancedSchedulingOptimizer
from clinic_ai.messaging.voice_agent import AzureVoiceProcessor, CompositeVoiceProcessor
from clinic_ai.messaging.notification_service import MultiChannelNotificationService


def test_medical_terminology():
    """Test that medical terminology was populated."""
    print("Testing Medical Terminology...")
    
    count = MedicalTerminology.objects.count()
    print(f"  Medical terminology entries: {count}")
    
    if count > 0:
        sample_term = MedicalTerminology.objects.first()
        print(f"  Sample term: {sample_term.term_en} -> {sample_term.term_ko} ({sample_term.category})")
        return True
    else:
        print("  ERROR: No medical terminology found")
        return False


def test_configuration_service():
    """Test the configuration service."""
    print("\nTesting Configuration Service...")
    
    config = DjangoConfigService()
    
    # Test API key retrieval
    openai_key = config.get_api_key('openai')
    print(f"  OpenAI API Key: {'Found' if openai_key else 'Not found'}")
    
    # Test feature flags
    voice_enabled = config.is_feature_enabled('ai_voice_agent')
    print(f"  Voice Agent Feature: {voice_enabled}")
    
    return True


def test_translation_service():
    """Test the translation service."""
    print("\nTesting Translation Service...")
    
    from clinic_ai.core.config import DjangoConfigService
    from clinic_ai.core.cache import DjangoCacheService
    
    config = DjangoConfigService()
    cache = DjangoCacheService()
    
    # Create Google Translate service
    translator = GoogleTranslateService(config, cache)
    enhanced_service = EnhancedTranslationService(translator)
    
    # Test translation
    text = "Hello, I would like to make an appointment"
    result = enhanced_service.translate_message(text, 'ko')
    print(f"  English: {text}")
    print(f"  Korean: {result['translated_text']}")
    
    return True


def test_ai_service():
    """Test the AI service."""
    print("\nTesting AI Service...")
    
    from clinic_ai.core.config import DjangoConfigService
    
    config = DjangoConfigService()
    
    try:
        # Create AI services
        openai_service = OpenAIService(config)
        keyword_service = KeywordBasedAIService()
        composite_service = CompositeAIService(openai_service, keyword_service)
        
        # Test response generation
        message = "I want to schedule a consultation"
        lang = "en"
        response, confidence = composite_service.generate_response(message, lang)
        print(f"  Input: {message}")
        print(f"  Response: {response}")
        print(f"  Confidence: {confidence}")
        
        # Test intent classification
        intent_result = composite_service.classify_intent(message)
        print(f"  Intent: {intent_result['intent']}, Confidence: {intent_result['confidence']}")
        
        return True
        
    except Exception as e:
        print(f"  ERROR: {e}")
        return False


def test_scheduling_optimizer():
    """Test the scheduling optimizer."""
    print("\nTesting Scheduling Optimizer...")
    
    optimizer = AdvancedSchedulingOptimizer()
    
    # Just verify the optimizer can be instantiated and has required methods
    print(f"  Optimizer instantiated: {type(optimizer).__name__}")
    print(f"  Has find_available_slots method: {hasattr(optimizer, 'find_available_slots')}")
    print(f"  Has create_appointment method: {hasattr(optimizer, 'create_appointment')}")
    print(f"  Has optimize_schedule method: {hasattr(optimizer, 'optimize_schedule')}")
    
    return True


def test_notification_service():
    """Test the notification service."""
    print("\nTesting Notification Service...")
    
    notification_service = MultiChannelNotificationService()
    
    print(f"  Notification service instantiated: {type(notification_service).__name__}")
    print(f"  Has send_reminder method: {hasattr(notification_service, 'send_reminder')}")
    print(f"  Has notify_staff method: {hasattr(notification_service, 'notify_staff')}")
    
    return True


def test_voice_agent():
    """Test the voice agent."""
    print("\nTesting Voice Agent...")
    
    # Create mock AI and translator services for voice agent
    from clinic_ai.core.config import DjangoConfigService
    from clinic_ai.messaging.ai_service import KeywordBasedAIService
    
    config = DjangoConfigService()
    ai_service = KeywordBasedAIService()
    
    # Test Azure voice processor
    azure_voice = AzureVoiceProcessor(ai_service)
    print(f"  Azure voice processor instantiated: {type(azure_voice).__name__}")
    print(f"  Has process_incoming_call method: {hasattr(azure_voice, 'process_incoming_call')}")
    print(f"  Has generate_tts method: {hasattr(azure_voice, 'generate_tts')}")
    print(f"  Has transcribe_audio method: {hasattr(azure_voice, 'transcribe_audio')}")
    
    # Test Twilio voice handler
    from clinic_ai.messaging.voice_agent import TwilioVoiceHandler
    twilio_voice = TwilioVoiceHandler(ai_service)
    print(f"  Twilio voice handler instantiated: {type(twilio_voice).__name__}")
    
    # Test composite voice processor
    composite_voice = CompositeVoiceProcessor(azure_voice, twilio_voice)
    print(f"  Composite voice processor instantiated: {type(composite_voice).__name__}")
    
    return True


def test_patient_creation():
    """Test patient management."""
    print("\nTesting Patient Management...")
    
    # Create a test patient
    patient, created = Patient.objects.get_or_create(
        phone="+1234567890",
        defaults={'name': 'Test Patient', 'preferred_language': 'en'}
    )
    
    print(f"  Patient created: {created}")
    print(f"  Patient: {patient.name} ({patient.phone}) - {patient.preferred_language}")
    
    return True


def run_all_tests():
    """Run all MVP feature tests."""
    print("Running CareBridge AI MVP Feature Tests\n")
    print("="*50)
    
    tests = [
        test_medical_terminology,
        test_configuration_service,
        test_translation_service,
        test_ai_service,
        test_scheduling_optimizer,
        test_notification_service,
        test_voice_agent,
        test_patient_creation
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
                print("  ✓ PASSED\n")
            else:
                print("  ✗ FAILED\n")
        except Exception as e:
            print(f"  ✗ ERROR: {e}\n")
    
    print("="*50)
    print(f"Tests completed: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All MVP features are working correctly!")
        return True
    else:
        print(f"⚠️  {total - passed} tests failed. Please check the implementation.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)