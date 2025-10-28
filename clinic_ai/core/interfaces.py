"""
Abstract interfaces for the Hospital & Clinic Patient Management System.
Following Dependency Inversion Principle - high-level modules depend on abstractions.
Composition-enabled design with clear contracts.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, List, Any
from datetime import datetime


class MessageHandler(ABC):
    """
    Abstract interface for message handling across channels.
    Defines contract for channel-agnostic message processing.
    """

    @abstractmethod
    def send_message(self, recipient: str, content: str, language: str = 'ko') -> bool:
        """Send message via specific channel"""
        pass

    @abstractmethod
    def receive_message(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process incoming message from channel"""
        pass

    @property
    @abstractmethod
    def channel_name(self) -> str:
        """Return channel identifier"""
        pass


class LanguageDetector(ABC):
    """
    Abstract interface for language detection.
    Enables pluggable language detection implementations.
    """

    @abstractmethod
    def detect(self, text: str) -> str:
        """Detect language from text content"""
        pass


class Translator(ABC):
    """
    Abstract interface for text translation.
    Enables composition with different translation services.
    """

    @abstractmethod
    def translate(self, text: str, from_lang: str, to_lang: str) -> str:
        """Translate text between languages"""
        pass

    @abstractmethod
    def get_supported_languages(self) -> List[str]:
        """Return list of supported language codes"""
        pass


class AIService(ABC):
    """
    Abstract interface for AI-powered responses.
    Defines contract for pluggable AI implementations.
    """

    @abstractmethod
    def generate_response(self, message: str, language: str, context: Optional[Dict] = None) -> tuple[str, float]:
        """Generate AI response with confidence score"""
        pass

    @abstractmethod
    def classify_intent(self, message: str) -> Dict[str, Any]:
        """Classify user intent from message"""
        pass


class VoiceProcessor(ABC):
    """
    Abstract interface for voice call processing.
    Enables composition with different voice providers.
    """

    @abstractmethod
    def process_incoming_call(self, phone_number: str) -> Dict[str, Any]:
        """Handle incoming voice call"""
        pass

    @abstractmethod
    def generate_tts(self, text: str, language: str) -> bytes:
        """Generate text-to-speech audio"""
        pass

    @abstractmethod
    def transcribe_audio(self, audio_data: bytes, language: str) -> str:
        """Transcribe audio to text"""
        pass


class Scheduler(ABC):
    """
    Abstract interface for appointment scheduling.
    Defines contract for scheduling algorithms.
    """

    @abstractmethod
    def find_available_slots(self, doctor: str, date_range: tuple[datetime, datetime],
                           preferences: Optional[Dict] = None) -> List[datetime]:
        """Find available appointment slots"""
        pass

    @abstractmethod
    def create_appointment(self, patient_id: str, doctor: str, procedure: str,
                          scheduled_at: datetime) -> Dict[str, Any]:
        """Create new appointment"""
        pass

    @abstractmethod
    def optimize_schedule(self, appointments: List[Dict]) -> List[Dict]:
        """Optimize appointment schedule for efficiency"""
        pass


class NotificationService(ABC):
    """
    Abstract interface for sending notifications.
    Enables multiple notification channels.
    """

    @abstractmethod
    def send_reminder(self, appointment_id: str, patient_contact: str, message: str) -> bool:
        """Send appointment reminder"""
        pass

    @abstractmethod
    def notify_staff(self, message: str, priority: str = 'normal') -> bool:
        """Notify staff about system events"""
        pass


class MetricsCollector(ABC):
    """
    Abstract interface for collecting system metrics.
    Enables pluggable metrics implementations.
    """

    @abstractmethod
    def record_message(self, message_data: Dict[str, Any]) -> None:
        """Record message-related metrics"""
        pass

    @abstractmethod
    def record_appointment(self, appointment_data: Dict[str, Any]) -> None:
        """Record appointment-related metrics"""
        pass

    @abstractmethod
    def get_daily_metrics(self, date: datetime) -> Dict[str, Any]:
        """Retrieve daily performance metrics"""
        pass


class CacheService(ABC):
    """
    Abstract interface for caching operations.
    Enables pluggable cache implementations.
    """

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Retrieve value from cache"""
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Store value in cache with optional TTL"""
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        """Remove value from cache"""
        pass


class ConfigurationService(ABC):
    """
    Abstract interface for configuration management.
    Enables environment-specific config handling.
    """

    @abstractmethod
    def get_api_key(self, service_name: str) -> str:
        """Retrieve API key for external service"""
        pass

    @abstractmethod
    def get_setting(self, key: str, default: Optional[Any] = None) -> Any:
        """Retrieve configuration setting"""
        pass

    @abstractmethod
    def is_feature_enabled(self, feature_name: str) -> bool:
        """Check if feature flag is enabled"""
        pass