"""
Pytest configuration and shared fixtures for CareBridge AI tests
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, MagicMock


# ============================================================================
# Customer Personas (from real sample data)
# ============================================================================

@pytest.fixture
def japanese_customer_persona():
    """Japanese customer persona based on real chat log (NAK*********)"""
    return {
        "name": "NAK*********",
        "language": "ja",
        "nationality": "日本",
        "service_requested": "nose_consultation",
        "previous_experience": "唇フィラー",
        "found_via": "Twitter",
        "cannot_bring_interpreter": True,
        "requests_time_change": True,
        "typical_messages": [
            "鼻のカウンセリングを検討しております",
            "通訳者を連れていくことが難しいのですが大丈夫でしょうか?",
            "14:00頃に変更は可能でしょうか?",
            "予定通りに伺います"
        ]
    }


@pytest.fixture
def chinese_customer_persona():
    """Chinese (Taiwanese) customer persona based on real chat log (Huang ****)"""
    return {
        "name_cn": "黃嘉怡",
        "name_en": "Huang Chia-Yi",
        "language": "zh",
        "nationality": "台灣",
        "is_returning_customer": True,
        "books_for_groups": True,
        "asks_many_questions": True,
        "found_via": "Instagram",
        "experiences_delay": True,
        "typical_messages": [
            "咀嚼肌肉毒的價錢",
            "請問諮詢的話是諮詢師看完後院長會再評估一次嗎?",
            "中文服務都會陪同整個過程嗎?",
            "我們在捷運站 因為新沙悠遊卡問題卡住",
            "我們今年三月去過"
        ],
        "previous_visits": [
            {
                "date": "2025-03-06",
                "procedures": ["電音波", "咀嚼肌肉毒", "嘴唇玻尿酸"]
            }
        ]
    }


# ============================================================================
# Appointment Fixtures
# ============================================================================

@pytest.fixture
def single_appointment():
    """Single person appointment"""
    return {
        "id": "appt_001",
        "date": "2025-11-05",
        "time": "17:00",
        "patient": {
            "name": "NAK*********",
            "phone": "+81-90-1234-5678",
            "language": "ja"
        },
        "service": "nose_consultation",
        "status": "confirmed"
    }


@pytest.fixture
def group_appointment():
    """Multi-person appointment"""
    return {
        "id": "appt_002",
        "date": "2025-03-06",
        "people": [
            {
                "name_cn": "黃嘉怡",
                "name_en": "Huang Chia-Yi",
                "time": "10:00"
            },
            {
                "name_cn": "楊君璦",
                "name_en": "Yang Chun-Ai",
                "time": "10:00"
            },
            {
                "name_cn": "江宜卉",
                "name_en": "Chiang Yi-Hui",
                "time": "11:30"
            }
        ],
        "language": "zh",
        "status": "confirmed"
    }


@pytest.fixture
def appointment_with_time_change(single_appointment):
    """Appointment that has been rescheduled"""
    appt = single_appointment.copy()
    appt["original_time"] = "17:00"
    appt["time"] = "14:00"
    appt["change_history"] = [
        {
            "timestamp": datetime.now() - timedelta(days=1),
            "from_time": "17:00",
            "to_time": "14:00",
            "requested_by": "patient"
        }
    ]
    return appt


# ============================================================================
# Calendar and Availability Fixtures
# ============================================================================

@pytest.fixture
def calendar_fully_booked():
    """Calendar with fully booked dates"""
    return {
        "2025-03-07": {"status": "full"},
        "2025-11-15": {"status": "full"}
    }


@pytest.fixture
def calendar_partially_available():
    """Calendar with partial availability"""
    return {
        "2025-03-06": {
            "status": "partial",
            "slots": {
                "10:00": {"capacity": 2, "booked": 0},
                "11:30": {"capacity": 1, "booked": 0}
            }
        }
    }


@pytest.fixture
def calendar_fully_available():
    """Calendar with full availability"""
    return {
        "2025-11-13": {
            "status": "available",
            "slots": {
                "10:00": {"capacity": 3, "booked": 0},
                "14:00": {"capacity": 3, "booked": 0},
                "17:00": {"capacity": 3, "booked": 0}
            }
        }
    }


# ============================================================================
# Message and Conversation Fixtures
# ============================================================================

@pytest.fixture
def price_inquiry_messages():
    """Price inquiry message examples"""
    return {
        "chinese": [
            "咀嚼肌肉毒的價錢",
            "咀嚼肌肉毒、嘴唇玻尿酸 、美版超聲刀 的價錢",
            "請問單純打咀嚼肌肉毒 費用是多少呢？"
        ],
        "japanese": [
            "価格を教えてください",
            "料金はいくらですか"
        ]
    }


@pytest.fixture
def consultation_request_messages():
    """Consultation request examples"""
    return {
        "japanese": [
            "鼻のカウンセリングを検討しております",
            "カウンセリングの予約をしたいです"
        ],
        "chinese": [
            "想預約諮詢",
            "我想諮詢"
        ]
    }


@pytest.fixture
def delay_notification_messages():
    """Delay notification examples"""
    return {
        "chinese": [
            "不好意思我們在捷運站 因為新沙悠遊卡問題卡住 稍等我們一下 不好意思",
            "我們出來了！上樓中 謝謝你"
        ]
    }


# ============================================================================
# Medical Terminology Fixtures
# ============================================================================

@pytest.fixture
def medical_terms():
    """Medical terminology in multiple languages"""
    return {
        "nose_surgery": {
            "ko": "코 성형",
            "ja": "鼻整形",
            "zh": "鼻整形",
            "en": "nose surgery"
        },
        "botox": {
            "ko": "보톡스",
            "ja": "ボトックス",
            "zh": "肉毒",
            "en": "botox"
        },
        "filler": {
            "ko": "히알루론산 필러",
            "ja": "ヒアルロン酸フィラー",
            "zh": "玻尿酸",
            "en": "hyaluronic acid filler"
        },
        "aftercare": {
            "ko": "사후관리",
            "ja": "術後ケア",
            "zh": "術後護理",
            "en": "aftercare"
        },
        "swelling": {
            "ko": "부기",
            "ja": "腫れ",
            "zh": "腫脹",
            "en": "swelling"
        },
        "jawline_botox": {
            "ko": "사각턱 보톡스",
            "ja": "咀嚼筋ボトックス",
            "zh": "咀嚼肌肉毒",
            "en": "jawline botox"
        }
    }


# ============================================================================
# Service and Configuration Fixtures
# ============================================================================

@pytest.fixture
def business_hours():
    """Business hours configuration"""
    return {
        "monday": {"start": "10:00", "end": "19:00"},
        "tuesday": {"start": "10:00", "end": "19:00"},
        "wednesday": {"start": "10:00", "end": "19:00"},
        "thursday": {"start": "10:00", "end": "19:00"},
        "friday": {"start": "10:00", "end": "19:00"},
        "saturday": {"start": "10:00", "end": "16:00"},  # Chinese
        "saturday_ja": {"start": "10:00", "end": "17:00"},  # Japanese
        "sunday": None,  # Closed
        "holidays": []  # List of holiday dates
    }


@pytest.fixture
def pricing_info():
    """Pricing information for various services"""
    return {
        "botox": {
            "korean_botulax": {"price": 99000, "currency": "KRW", "area": "咀嚼肌"},
            "german_xeomin": {"price": 220000, "currency": "KRW", "area": "咀嚼肌"}
        },
        "filler": {
            "korean_bellast": {"price": 165000, "currency": "KRW", "volume": "1cc"},
            "korean_chaeum": {"price": 165000, "currency": "KRW", "volume": "1cc"},
            "lips": {"price": 220000, "currency": "KRW", "volume": "1cc"}
        },
        "consultation": {
            "counselor": {"price": 0, "currency": "KRW"},
            "doctor": {"price": 10000, "currency": "KRW", "refundable": True}
        }
    }


# ============================================================================
# Mock Services
# ============================================================================

@pytest.fixture
def mock_translation_service():
    """Mock translation service"""
    service = Mock()
    service.translate.return_value = "Translated text"
    service.detect_language.return_value = {"language": "ja", "confidence": 0.95}
    return service


@pytest.fixture
def mock_ai_service():
    """Mock AI service"""
    service = Mock()
    service.classify_intent.return_value = {
        "intent": "consultation_request",
        "confidence": 0.9
    }
    service.generate_response.return_value = ("Response text", 0.85)
    return service


@pytest.fixture
def mock_calendar_service():
    """Mock calendar service"""
    service = Mock()
    service.check_availability.return_value = True
    service.book_appointment.return_value = {"success": True, "id": "appt_123"}
    service.update_appointment.return_value = {"success": True}
    return service


# ============================================================================
# Helper Functions
# ============================================================================

def create_message(text, language, phone=None, timestamp=None):
    """Helper to create test message"""
    return {
        "text": text,
        "language": language,
        "phone": phone or "+82-10-1234-5678",
        "timestamp": timestamp or datetime.now()
    }


def create_booking_data(language="zh", complete=True):
    """Helper to create booking data"""
    data = {
        "name_cn": "Test User",
        "name_en": "TEST USER",
        "dob": "1990-01-01",
        "gender": "F",
        "nationality": "台灣" if language == "zh" else "日本"
    }
    if complete:
        data.update({
            "contact": "+886-912-345-678",
            "recent_procedures": "無",
            "consultation_items": "肉毒",
            "same_day_procedure": "是",
            "sedation": "否"
        })
    return data


# Make helper functions available to tests
pytest.create_message = create_message
pytest.create_booking_data = create_booking_data
