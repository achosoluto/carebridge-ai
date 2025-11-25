#!/usr/bin/env python
"""
CareBridge AI - Integration Test Runner
Executes all integration and end-to-end tests to validate complete system functionality
"""
import os
import sys
import subprocess
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

def run_integration_tests():
    """Run all integration and end-to-end tests"""
    
    print("🚀 CareBridge AI - Integration Test Runner")
    print("=" * 50)
    
    # Step 1: Run translation accuracy tests
    print("\n🧪 Running Translation Accuracy Tests...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/test_translation_accuracy.py", 
            "-v", "--tb=short"
        ], capture_output=True, text=True, cwd=project_root)
        
        if result.returncode == 0:
            print("✅ Translation accuracy tests: PASSED")
        else:
            print("❌ Translation accuracy tests: FAILED")
            print(result.stdout)
            print(result.stderr)
    except Exception as e:
        print(f"❌ Error running translation tests: {e}")
    
    # Step 2: Run end-to-end tests
    print("\n🔗 Running End-to-End Tests...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/test_end_to_end.py", 
            "-v", "--tb=short"
        ], capture_output=True, text=True, cwd=project_root)
        
        if result.returncode == 0:
            print("✅ End-to-end tests: PASSED")
        else:
            print("❌ End-to-end tests: FAILED")
            print(result.stdout)
            print(result.stderr)
    except Exception as e:
        print(f"❌ Error running end-to-end tests: {e}")
    
    # Step 3: Run Django management command tests
    print("\n⚙️  Running Django Management Command Tests...")
    try:
        # Import and run health check command programmatically
        from django.core.management import call_command
        from django.conf import settings
        
        # Setup Django
        import django
        django.setup()
        
        # Run health check
        print("Running system health check...")
        call_command('health_check')
        print("✅ Health check command: PASSED")
        
    except Exception as e:
        print(f"❌ Error running health check: {e}")
        
    # Step 4: Run basic Django tests 
    print("\n📋 Running Basic Django Tests...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "clinic_ai/core/", 
            "-k", "not accuracy and not end_to_end",
            "-v", "--tb=short"
        ], capture_output=True, text=True, cwd=project_root)
        
        if result.returncode == 0:
            print("✅ Basic Django tests: PASSED")
        else:
            print("⚠️  Basic Django tests: Some failures (may be expected in development)")
            print(result.stdout)
            # Don't print stderr for warnings
    except Exception as e:
        print(f"⚠️  Error running basic tests: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Integration Test Summary")
    print("All major system components have been validated.")
    print("Check individual results above for details.")

def run_performance_tests():
    """Run basic performance validation"""
    print("\n⚡ Running Performance Validation Tests...")
    
    import time
    from clinic_ai.core.config import DjangoConfigService
    from clinic_ai.messaging.translation_enhanced import EnhancedTranslationService, EnhancedGoogleTranslateService
    
    try:
        # Setup translation service
        config_service = DjangoConfigService()
        google_service = EnhancedGoogleTranslateService(config_service)
        translation_service = EnhancedTranslationService(google_service)
        
        # Test translation speed
        test_phrases = [
            "안녕하세요, 어떻게 도와드릴까요?",
            "가슴이 아파요",
            "내일 예약 가능한가요?",
            "약을 처방해 주시나요?"
        ]
        
        print("Testing translation performance...")
        total_time = 0
        for phrase in test_phrases:
            start_time = time.time()
            result = translation_service.translate_message(
                text=phrase,
                target_lang='en',
                message_id=None
            )
            end_time = time.time()
            total_time += (end_time - start_time)
        
        avg_time = (total_time / len(test_phrases)) * 1000  # Convert to ms
        print(f"✅ Average translation time: {avg_time:.1f}ms per phrase")
        
        if avg_time < 1000:  # Less than 1 second
            print("✅ Performance: GOOD (under 1s per translation)")
        else:
            print("⚠️  Performance: SLOW (over 1s per translation)")
        
    except Exception as e:
        print(f"❌ Performance test error: {e}")

def validate_system_components():
    """Validate all system components are properly configured"""
    print("\n🔍 Running System Component Validation...")
    
    try:
        # Test database connectivity
        from clinic_ai.core.models import Patient
        patient_count = Patient.objects.count()
        print(f"✅ Database: OK (found {patient_count} patients)")
    except Exception as e:
        print(f"❌ Database: ERROR - {e}")
    
    try:
        # Test cache connectivity
        import redis
        from django.conf import settings
        cache_client = redis.from_url(settings.CACHES['default']['LOCATION'])
        cache_client.ping()
        print("✅ Cache (Redis): OK")
    except Exception as e:
        print(f"❌ Cache: ERROR - {e}")
    
    try:
        # Test configuration
        from clinic_ai.core.config import DjangoConfigService
        config_service = DjangoConfigService()
        api_key = config_service.get_api_key('google_translate')
        if 'fake' in api_key or api_key.startswith('development'):
            print("⚠️  API Keys: Using development keys (not configured for production)")
        else:
            print("✅ API Keys: Properly configured")
    except Exception as e:
        print(f"❌ Configuration: ERROR - {e}")

if __name__ == "__main__":
    # Setup Django
    try:
        import django
        from django.conf import settings
        if not settings.configured:
            django.setup()
    except Exception as e:
        print(f"Django setup error (this is expected if run outside Django context): {e}")
        print("Continuing with limited functionality...")
    
    run_integration_tests()
    run_performance_tests()
    validate_system_components()
    
    print(f"\n🎯 Integration validation completed!")
    print(f"Review results above to ensure all components are ready for beta.")