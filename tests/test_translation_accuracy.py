"""
Translation accuracy validation tests

Tests the core value proposition: accurate Korean ↔ English medical translation
Uses real Google Translate API (not mocked) to validate production accuracy
"""
import json
import pytest
from pathlib import Path
from difflib import SequenceMatcher
from clinic_ai.messaging.translation_enhanced import EnhancedTranslationService, EnhancedGoogleTranslateService
from clinic_ai.core.config import DjangoConfigService

def get_config_service():
    """Get configuration service for tests"""
    return DjangoConfigService()

# Load test fixtures
FIXTURES_PATH = Path(__file__).parent / 'fixtures' / 'korean_medical_phrases.json'

def load_test_phrases():
    """Load Korean medical phrase test cases"""
    with open(FIXTURES_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculate similarity between two strings (0.0 to 1.0)
    Uses SequenceMatcher for fuzzy matching
    """
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

@pytest.fixture
def translation_service():
    """Initialize translation service"""
    config_service = get_config_service()
    google_service = EnhancedGoogleTranslateService(config_service)
    return EnhancedTranslationService(google_service)

class TestTranslationAccuracy:
    """
    Translation accuracy validation tests

    Success criteria: ≥90% accuracy across all test cases
    """

    def test_korean_to_english_symptoms(self, translation_service):
        """Test Korean → English translation for symptom descriptions"""
        test_cases = [tc for tc in load_test_phrases() if tc['category'] == 'symptoms']

        results = []
        for test_case in test_cases:
            result = translation_service.translate_message(
                text=test_case['korean'],
                target_lang='en',
                message_id=None  # Not saving to history for tests
            )

            similarity = calculate_similarity(
                result['translated_text'],
                test_case['expected_english']
            )

            results.append({
                'korean': test_case['korean'],
                'expected': test_case['expected_english'],
                'actual': result['translated_text'],
                'similarity': similarity,
                'passed': similarity >= 0.80  # 80% similarity threshold
            })

        # Calculate overall accuracy
        accuracy = sum(r['passed'] for r in results) / len(results)

        # Log results
        print(f"\n{'='*80}")
        print(f"SYMPTOM TRANSLATION ACCURACY: {accuracy:.1%}")
        print(f"{'='*80}")
        for r in results:
            status = "✅" if r['passed'] else "❌"
            print(f"{status} {r['korean']} → {r['actual']} (similarity: {r['similarity']:.1%})")

        # Assert ≥90% accuracy
        assert accuracy >= 0.90, f"Symptom translation accuracy {accuracy:.1%} below 90% threshold"

    def test_korean_to_english_scheduling(self, translation_service):
        """Test Korean → English translation for scheduling phrases"""
        test_cases = [tc for tc in load_test_phrases() if tc['category'] == 'scheduling']

        results = []
        for test_case in test_cases:
            result = translation_service.translate_message(
                text=test_case['korean'],
                target_lang='en',
                message_id=None  # Not saving to history for tests
            )

            similarity = calculate_similarity(
                result['translated_text'],
                test_case['expected_english']
            )

            results.append({
                'korean': test_case['korean'],
                'expected': test_case['expected_english'],
                'actual': result['translated_text'],
                'similarity': similarity,
                'passed': similarity >= 0.80
            })

        accuracy = sum(r['passed'] for r in results) / len(results)

        print(f"\n{'='*80}")
        print(f"SCHEDULING TRANSLATION ACCURACY: {accuracy:.1%}")
        print(f"{'='*80}")
        for r in results:
            status = "✅" if r['passed'] else "❌"
            print(f"{status} {r['korean']} → {r['actual']} (similarity: {r['similarity']:.1%})")

        assert accuracy >= 0.90, f"Scheduling translation accuracy {accuracy:.1%} below 90% threshold"

    def test_english_to_korean_responses(self, translation_service):
        """Test English → Korean translation for clinic responses"""
        test_cases = [
            {
                'english': 'Your appointment is confirmed for tomorrow at 2 PM',
                'expected_korean': '내일 오후 2시 예약이 확인되었습니다',
            },
            {
                'english': 'Please arrive 15 minutes early',
                'expected_korean': '15분 일찍 도착해 주세요',
            },
            {
                'english': 'Bring your insurance card',
                'expected_korean': '보험 카드를 가져오세요',
            },
        ]

        results = []
        for test_case in test_cases:
            result = translation_service.translate_message(
                text=test_case['english'],
                target_lang='ko',
                message_id=None  # Not saving to history for tests
            )

            similarity = calculate_similarity(
                result['translated_text'],
                test_case['expected_korean']
            )

            results.append({
                'english': test_case['english'],
                'expected': test_case['expected_korean'],
                'actual': result['translated_text'],
                'similarity': similarity,
                'passed': similarity >= 0.70  # Lower threshold for Korean (harder to match exactly)
            })

        accuracy = sum(r['passed'] for r in results) / len(results)

        print(f"\n{'='*80}")
        print(f"RESPONSE TRANSLATION ACCURACY: {accuracy:.1%}")
        print(f"{'='*80}")
        for r in results:
            status = "✅" if r['passed'] else "❌"
            print(f"{status} {r['english']} → {r['actual']} (similarity: {r['similarity']:.1%})")

        assert accuracy >= 0.80, f"Response translation accuracy {accuracy:.1%} below 80% threshold"

    def test_overall_translation_accuracy(self, translation_service):
        """Test overall translation accuracy across all categories"""
        all_test_cases = load_test_phrases()

        results = []
        for test_case in all_test_cases:
            result = translation_service.translate_message(
                text=test_case['korean'],
                target_lang='en',
                message_id=None  # Not saving to history for tests
            )

            similarity = calculate_similarity(
                result['translated_text'],
                test_case['expected_english']
            )

            results.append({
                'category': test_case['category'],
                'korean': test_case['korean'],
                'expected': test_case['expected_english'],
                'actual': result['translated_text'],
                'similarity': similarity,
                'passed': similarity >= 0.80
            })

        # Calculate accuracy by category
        categories = set(r['category'] for r in results)
        category_accuracy = {}
        for category in categories:
            category_results = [r for r in results if r['category'] == category]
            category_accuracy[category] = sum(r['passed'] for r in category_results) / len(category_results)

        # Overall accuracy
        overall_accuracy = sum(r['passed'] for r in results) / len(results)

        # Print detailed report
        print(f"\n{'='*80}")
        print(f"OVERALL TRANSLATION ACCURACY REPORT")
        print(f"{'='*80}")
        print(f"\nOverall Accuracy: {overall_accuracy:.1%}")
        print(f"\nAccuracy by Category:")
        for category, accuracy in sorted(category_accuracy.items()):
            print(f"  {category:20s}: {accuracy:.1%}")

        print(f"\nDetailed Results:")
        for r in results:
            status = "✅" if r['passed'] else "❌"
            print(f"{status} [{r['category']:15s}] {r['korean']} → {r['actual']}")

        # Assert ≥90% overall accuracy
        assert overall_accuracy >= 0.90, (
            f"Overall translation accuracy {overall_accuracy:.1%} below 90% threshold\n"
            f"Category breakdown: {category_accuracy}"
        )