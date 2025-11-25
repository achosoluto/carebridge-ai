#!/usr/bin/env python
"""
CareBridge AI - Final Pre-Launch Validation Script
Comprehensive validation before beta launch to ensure system readiness.
"""
import os
import sys
import subprocess
import json
from datetime import datetime
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

def run_validation_tests():
    """Run all validation tests before launch"""
    
    print("🚀 CareBridge AI - Final Pre-Launch Validation")
    print("=" * 60)
    print(f"Validation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Project Root: {project_root}")
    print()
    
    validation_results = {
        'timestamp': datetime.now().isoformat(),
        'tests': []
    }
    
    # 1. Check environment and dependencies
    print("🔍 1. Checking Environment & Dependencies...")
    try:
        # Check Python version
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        print(f"   ✅ Python Version: {python_version}")
        
        # Check required packages
        import django
        import sentry_sdk
        import requests
        import redis
        
        print(f"   ✅ Django: {django.get_version()}")
        print(f"   ✅ Sentry SDK: Available")
        print(f"   ✅ Requests: Available")
        print(f"   ✅ Redis: Available")
        
        validation_results['tests'].append({
            'name': 'Environment Check',
            'status': 'PASS',
            'details': f'Python {python_version}, Django {django.get_version()}'
        })
    except ImportError as e:
        print(f"   ❌ Missing dependency: {e}")
        validation_results['tests'].append({
            'name': 'Environment Check',
            'status': 'FAIL',
            'details': str(e)
        })
    
    # 2. Run translation accuracy tests
    print("\n🔤 2. Running Translation Accuracy Tests...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/test_translation_accuracy.py", 
            "-v", "--tb=short", "-s"
        ], capture_output=True, text=True, cwd=project_root)
        
        if result.returncode == 0:
            print("   ✅ Translation Accuracy Tests: PASSED")
            validation_results['tests'].append({
                'name': 'Translation Accuracy Tests',
                'status': 'PASS',
                'details': 'All translation tests passed'
            })
        else:
            print("   ❌ Translation Accuracy Tests: FAILED")
            print(f"      Output: {result.stdout}")
            if result.stderr:
                print(f"      Errors: {result.stderr}")
            validation_results['tests'].append({
                'name': 'Translation Accuracy Tests',
                'status': 'FAIL',
                'details': result.stdout
            })
    except Exception as e:
        print(f"   ❌ Error running translation tests: {e}")
        validation_results['tests'].append({
            'name': 'Translation Accuracy Tests',
            'status': 'FAIL',
            'details': str(e)
        })
    
    # 3. Run end-to-end tests
    print("\n🔗 3. Running End-to-End Tests...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/test_end_to_end.py", 
            "-v", "--tb=short"
        ], capture_output=True, text=True, cwd=project_root)
        
        if result.returncode == 0:
            print("   ✅ End-to-End Tests: PASSED")
            validation_results['tests'].append({
                'name': 'End-to-End Tests',
                'status': 'PASS',
                'details': 'All E2E tests passed'
            })
        else:
            print("   ❌ End-to-End Tests: FAILED")
            print(f"      Output: {result.stdout}")
            validation_results['tests'].append({
                'name': 'End-to-End Tests',
                'status': 'FAIL',
                'details': result.stdout
            })
    except Exception as e:
        print(f"   ❌ Error running E2E tests: {e}")
        validation_results['tests'].append({
            'name': 'End-to-End Tests',
            'status': 'FAIL',
            'details': str(e)
        })
    
    # 4. Run Django management command (health check)
    print("\n⚙️  4. Running System Health Check...")
    try:
        # Import Django components
        import django
        django.setup()
        
        from django.core.management import call_command
        from io import StringIO
        import contextlib
        
        # Capture the output of the health check
        f = StringIO()
        with contextlib.redirect_stdout(f):
            call_command('health_check')
        health_output = f.getvalue()
        
        if "all checks passed" in health_output.lower() or "system is healthy" in health_output.lower():
            print("   ✅ Health Check: PASSED")
            validation_results['tests'].append({
                'name': 'System Health Check',
                'status': 'PASS',
                'details': 'All health checks passed'
            })
        else:
            print("   ⚠️  Health Check: PARTIAL (review output)")
            print(f"      Output: {health_output}")
            validation_results['tests'].append({
                'name': 'System Health Check',
                'status': 'WARN',
                'details': health_output
            })
    except Exception as e:
        print(f"   ❌ Health Check: ERROR - {e}")
        validation_results['tests'].append({
            'name': 'System Health Check',
            'status': 'FAIL',
            'details': str(e)
        })
    
    # 5. Check documentation completeness
    print("\n📚 5. Checking Documentation Completeness...")
    docs_to_check = [
        "docs/beta_onboarding_guide.md",
        "docs/beta_faq.md", 
        "docs/beta_launch_checklist.md",
        "docs/beta_onboarding_process.md",
        "docs/translation_accuracy_report.md"
    ]
    
    missing_docs = []
    for doc in docs_to_check:
        if (project_root / doc).exists():
            print(f"   ✅ {doc}: Available")
        else:
            print(f"   ❌ {doc}: MISSING")
            missing_docs.append(doc)
    
    if not missing_docs:
        validation_results['tests'].append({
            'name': 'Documentation Check',
            'status': 'PASS',
            'details': f'All {len(docs_to_check)} required documents present'
        })
    else:
        validation_results['tests'].append({
            'name': 'Documentation Check',
            'status': 'FAIL',
            'details': f'Missing documents: {", ".join(missing_docs)}'
        })
    
    # 6. Verify required files exist
    print("\n📄 6. Checking Required Files...")
    required_files = [
        "railway.json",
        ".env.example", 
        "requirements.txt",
        "manage.py",
        "config/settings.py"
    ]
    
    missing_files = []
    for file in required_files:
        if (project_root / file).exists():
            print(f"   ✅ {file}: Present")
        else:
            print(f"   ❌ {file}: MISSING")
            missing_files.append(file)
    
    if not missing_files:
        validation_results['tests'].append({
            'name': 'File Completeness Check',
            'status': 'PASS',
            'details': f'All {len(required_files)} required files present'
        })
    else:
        validation_results['tests'].append({
            'name': 'File Completeness Check',
            'status': 'FAIL',
            'details': f'Missing files: {", ".join(missing_files)}'
        })
    
    # 7. Check settings and configuration
    print("\n🔧 7. Checking Configuration Settings...")
    try:
        import django
        if not django.conf.settings.configured:
            django.setup()
        
        from django.conf import settings
        
        # Check key settings
        checks = [
            ("SECRET_KEY", bool(settings.SECRET_KEY and settings.SECRET_KEY != 'django-insecure-carebridge-ai-development-key')),
            ("DEBUG", hasattr(settings, 'DEBUG')),
            ("Database Config", hasattr(settings, 'DATABASES')),
            ("Sentry Config", hasattr(settings, 'SENTRY_DSN')),
            ("Cache Config", hasattr(settings, 'CACHES')),
            ("ALLOWED_HOSTS", bool(settings.ALLOWED_HOSTS)),
        ]
        
        config_issues = []
        for check_name, check_result in checks:
            if check_result:
                print(f"   ✅ {check_name}: Configured")
            else:
                print(f"   ⚠️  {check_name}: Not properly configured")
                config_issues.append(check_name)
        
        if not config_issues:
            validation_results['tests'].append({
                'name': 'Configuration Check',
                'status': 'PASS',
                'details': 'All critical settings configured'
            })
        else:
            validation_results['tests'].append({
                'name': 'Configuration Check',
                'status': 'WARN',
                'details': f'Configuration issues: {", ".join(config_issues)}'
            })
    except Exception as e:
        print(f"   ❌ Configuration Check: ERROR - {e}")
        validation_results['tests'].append({
            'name': 'Configuration Check',
            'status': 'FAIL',
            'details': str(e)
        })
    
    # 8. Performance validation
    print("\n⚡ 8. Running Performance Validation...")
    try:
        import time
        from clinic_ai.core.config import DjangoConfigService
        from clinic_ai.messaging.translation_enhanced import EnhancedTranslationService, EnhancedGoogleTranslateService
        
        # Setup translation service
        config_service = DjangoConfigService()
        google_service = EnhancedGoogleTranslateService(config_service)
        translation_service = EnhancedTranslationService(google_service)
        
        # Test a few translations to validate performance
        test_phrases = [
            "안녕하세요",
            "가슴이 아파요", 
            "내일 예약 가능한가요?"
        ]
        
        total_time = 0
        valid_translations = 0
        
        for phrase in test_phrases:
            start_time = time.time()
            try:
                result = translation_service.translate_message(
                    text=phrase,
                    target_lang='en',
                    message_id=None
                )
                end_time = time.time()
                
                total_time += (end_time - start_time)
                
                if result.get('translated_text'):
                    valid_translations += 1
            except Exception:
                continue  # Skip failed ones
        
        avg_time_ms = (total_time / len(test_phrases)) * 1000 if test_phrases else 0
        
        print(f"   ✅ Average Translation Time: {avg_time_ms:.0f}ms")
        print(f"   ✅ Successful Translations: {valid_translations}/{len(test_phrases)}")
        
        if avg_time_ms < 2000 and valid_translations == len(test_phrases):  # Less than 2 seconds
            validation_results['tests'].append({
                'name': 'Performance Validation',
                'status': 'PASS',
                'details': f'Avg {avg_time_ms:.0f}ms, {valid_translations} successful'
            })
        else:
            validation_results['tests'].append({
                'name': 'Performance Validation',
                'status': 'FAIL',
                'details': f'Avg {avg_time_ms:.0f}ms, {valid_translations}/{len(test_phrases)} successful'
            })
    except Exception as e:
        print(f"   ❌ Performance Validation: ERROR - {e}")
        validation_results['tests'].append({
            'name': 'Performance Validation',
            'status': 'FAIL',
            'details': str(e)
        })
    
    # Summarize results
    print(f"\n{'='*60}")
    print("📋 VALIDATION SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for t in validation_results['tests'] if t['status'] == 'PASS')
    failed = sum(1 for t in validation_results['tests'] if t['status'] == 'FAIL')
    warnings = sum(1 for t in validation_results['tests'] if t['status'] == 'WARN')
    
    print(f"Total Tests: {len(validation_results['tests'])}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Warnings: {warnings}")
    
    if failed == 0:
        print(f"\n🎉 OVERALL RESULT: ✅ READY FOR BETA LAUNCH")
        validation_results['overall'] = 'PASS'
    else:
        print(f"\n🚨 OVERALL RESULT: ❌ NOT READY FOR BETA LAUNCH")
        validation_results['overall'] = 'FAIL'
        print("\nFailed tests need to be addressed before launch:")
        for test in validation_results['tests']:
            if test['status'] == 'FAIL':
                print(f"  - {test['name']}: {test['details']}")
    
    # Save validation results to file
    validation_file = project_root / "validation_results.json"
    with open(validation_file, 'w', encoding='utf-8') as f:
        json.dump(validation_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Validation results saved to: {validation_file}")
    
    return validation_results['overall'] == 'PASS'

def main():
    """Main function to run the pre-launch validation"""
    try:
        is_ready = run_validation_tests()
        
        if is_ready:
            print(f"\n🚀 All validations passed! System is ready for beta launch.")
            sys.exit(0)
        else:
            print(f"\n❌ Some validations failed. Address issues before launch.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️  Validation interrupted by user.")
        sys.exit(2)
    except Exception as e:
        print(f"\n💥 Unexpected error during validation: {e}")
        sys.exit(3)

if __name__ == "__main__":
    main()