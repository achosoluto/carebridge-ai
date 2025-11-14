"""
Configuration service implementation for CareBridge AI.
Manages external service credentials and feature flags.
"""

import os
from typing import Any, Optional
from decouple import config
from ..core.interfaces import ConfigurationService


class DjangoConfigService(ConfigurationService):
    """
    Django-based configuration service implementation.
    Retrieves settings from environment variables and Django settings.
    """

    def get_api_key(self, service_name: str) -> str:
        """
        Retrieve API key for external service.

        Args:
            service_name: Name of the service (openai, google_translate, etc.)

        Returns:
            API key string
        """
        key_mapping = {
            'openai': 'OPENAI_API_KEY',
            'google_translate': 'GOOGLE_TRANSLATE_API_KEY',
            'kakao': 'KAKAO_API_KEY',
            'line': 'LINE_CHANNEL_ACCESS_TOKEN',
            'azure_speech': 'AZURE_SPEECH_KEY',
            'twilio': 'TWILIO_AUTH_TOKEN'
        }

        env_var = key_mapping.get(service_name.lower())
        if not env_var:
            raise ValueError(f"Unknown service name: {service_name}")

        api_key = config(env_var, default='')
        
        if not api_key:
            # For development, return mock keys
            dev_keys = {
                'OPENAI_API_KEY': 'sk-fake-openai-key-for-development',
                'GOOGLE_TRANSLATE_API_KEY': 'fake-google-translate-key-for-dev',
                'KAKAO_API_KEY': 'fake-kakao-key-for-dev',
                'LINE_CHANNEL_ACCESS_TOKEN': 'fake-line-token-for-dev',
                'AZURE_SPEECH_KEY': 'fake-azure-key-for-dev',
                'TWILIO_AUTH_TOKEN': 'fake-twilio-token-for-dev'
            }
            return dev_keys.get(env_var, 'development-key-not-set')
        
        return api_key

    def get_setting(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Retrieve configuration setting.

        Args:
            key: Setting key name
            default: Default value if not found

        Returns:
            Setting value
        """
        return config(key, default=default)

    def is_feature_enabled(self, feature_name: str) -> bool:
        """
        Check if feature flag is enabled.

        Args:
            feature_name: Name of the feature

        Returns:
            True if enabled, False otherwise
        """
        feature_flags = {
            'ai_voice_agent': 'ENABLE_VOICE_AGENT',
            'multi_channel_messaging': 'ENABLE_MESSAGING',
            'advanced_translation': 'ENABLE_ADVANCED_TRANSLATION',
            'scheduling_optimization': 'ENABLE_SCHEDULING_OPTIMIZATION',
            'waitlist_management': 'ENABLE_WAITLIST'
        }

        env_var = feature_flags.get(feature_name.lower())
        if not env_var:
            return False

        return config(env_var, default=True, cast=bool)


class MockConfigService(ConfigurationService):
    """
    Mock configuration service for testing and development.
    Returns predefined values without external dependencies.
    """

    MOCK_KEYS = {
        'openai': 'sk-test-openai-key',
        'google_translate': 'test-google-translate-key',
        'kakao': 'test-kakao-key',
        'line': 'test-line-channel-token',
        'azure_speech': 'test-azure-speech-key',
        'twilio': 'test-twilio-token'
    }

    def get_api_key(self, service_name: str) -> str:
        """Return mock API key for testing."""
        return self.MOCK_KEYS.get(service_name.lower(), 'mock-api-key')

    def get_setting(self, key: str, default: Optional[Any] = None) -> Any:
        """Return mock setting value."""
        # Return reasonable defaults for common settings
        defaults = {
            'DEFAULT_LANGUAGE': 'ko',
            'MAX_MESSAGE_LENGTH': 1000,
            'TRANSLATION_CACHE_TTL': 3600,
            'AI_CONFIDENCE_THRESHOLD': 0.7
        }
        
        return defaults.get(key, default)

    def is_feature_enabled(self, feature_name: str) -> bool:
        """Return True for all features in mock service."""
        return True


# Factory function to create appropriate config service
def create_config_service(use_mock: bool = False) -> ConfigurationService:
    """
    Factory function to create configuration service instance.
    
    Args:
        use_mock: If True, returns mock service; otherwise returns real service
    
    Returns:
        ConfigurationService instance
    """
    if use_mock:
        return MockConfigService()
    else:
        return DjangoConfigService()