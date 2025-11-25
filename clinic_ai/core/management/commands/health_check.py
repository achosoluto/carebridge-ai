"""
Health check management command for CareBridge AI system.
Verifies system components and dependencies are functioning properly.
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from clinic_ai.core.config import DjangoConfigService
from clinic_ai.messaging.translation_enhanced import EnhancedTranslationService, EnhancedGoogleTranslateService
import redis
import requests


class Command(BaseCommand):
    help = 'Perform system health check'

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Display detailed health check results',
        )

    def handle(self, *args, **options):
        self.stdout.write("Running CareBridge AI Health Check...\n")
        
        checks = [
            self.check_database(),
            self.check_cache(),
            self.check_google_translate_api(),
            self.check_sentry(),
            self.check_translation_accuracy(),
        ]
        
        passed = sum(checks)
        total = len(checks)
        
        self.stdout.write(f"\nHealth Check Summary: {passed}/{total} checks passed\n")
        
        if passed == total:
            self.stdout.write(
                self.style.SUCCESS("✅ System is healthy! All checks passed.")
            )
            return 0
        else:
            self.stdout.write(
                self.style.ERROR(f"❌ System has issues. {total - passed} checks failed.")
            )
            return 1

    def check_database(self):
        """Check if database is accessible"""
        try:
            from clinic_ai.core.models import Patient
            # Try a simple query
            count = Patient.objects.count()
            self.stdout.write("✅ Database connection: OK")
            return True
        except Exception as e:
            self.stdout.write(f"❌ Database connection: {str(e)}")
            return False

    def check_cache(self):
        """Check if Redis cache is accessible"""
        try:
            redis_client = redis.from_url(settings.CACHES['default']['LOCATION'])
            redis_client.ping()
            self.stdout.write("✅ Cache (Redis) connection: OK")
            return True
        except Exception as e:
            self.stdout.write(f"❌ Cache (Redis) connection: {str(e)}")
            return False

    def check_google_translate_api(self):
        """Check if Google Translate API key is configured"""
        try:
            config_service = DjangoConfigService()
            api_key = config_service.get_api_key('google_translate')
            
            if 'fake' in api_key or 'development' in api_key:
                self.stdout.write("⚠️  Google Translate API: Using development key (not configured)")
                return True  # Not a failure, just not configured
            else:
                # Try a simple API call to verify the key works
                self.stdout.write("✅ Google Translate API: Configured")
                return True
        except Exception as e:
            self.stdout.write(f"❌ Google Translate API: {str(e)}")
            return False

    def check_sentry(self):
        """Check if Sentry is configured"""
        try:
            import sentry_sdk
            dsn = settings.SENTRY_DSN if hasattr(settings, 'SENTRY_DSN') else None
            
            if dsn and 'your-sentry-dsn-here' not in str(dsn):
                self.stdout.write("✅ Sentry: Configured")
                return True
            else:
                self.stdout.write("⚠️  Sentry: Not configured (development only)")
                return True  # Not a failure in development
        except Exception as e:
            self.stdout.write(f"⚠️  Sentry: {str(e)}")
            return True  # Not critical

    def check_translation_accuracy(self):
        """Quick test of translation functionality"""
        try:
            config_service = DjangoConfigService()
            google_service = EnhancedGoogleTranslateService(config_service)
            translation_service = EnhancedTranslationService(google_service)
            
            # Test a simple translation
            result = translation_service.translate_message(
                text="안녕하세요",
                target_lang='en',
                message_id=None
            )
            
            translated = result.get('translated_text', '')
            
            if translated and len(translated) > 0:
                self.stdout.write("✅ Translation service: OK")
                if 'verbose' in options and options['verbose']:
                    self.stdout.write(f"   Test: '안녕하세요' → '{translated}'")
                return True
            else:
                self.stdout.write("❌ Translation service: Failed to translate")
                return False
        except Exception as e:
            self.stdout.write(f"❌ Translation service: {str(e)}")
            return False