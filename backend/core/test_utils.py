from rest_framework.authentication import BaseAuthentication

class MockStaffAuthentication(BaseAuthentication):
    """
    Mock authentication class for testing purposes.
    Assumes a 'testuser' exists and authenticates as that user.
    """
    def authenticate(self, request):
        from django.contrib.auth.models import User
        user, _ = User.objects.get_or_create(
            username='testuser',
            defaults={'is_staff': True, 'is_superuser': True}
        )
        return (user, None)

class MockTranslationService:
    def translate_text(self, text, target_language, source_language):
        return f"{text}[mock_translated]"