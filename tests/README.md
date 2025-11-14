# CareBridge AI Test Suite

Comprehensive test suite based on real customer chat log analysis from Japanese and Chinese (Traditional) customers.

## Overview

This test suite contains **250+ unit tests** covering:
- Conversation flows
- Multilingual support (Japanese, Chinese, Korean, English)
- Appointment management
- Edge cases and error handling
- Integration scenarios

All tests are derived from real customer interactions documented in `sample_data/` and mapped to test cases in `sample_data/test_cases.md`.

## Test Structure

```
tests/
├── __init__.py                          # Test package initialization
├── conftest.py                          # Shared fixtures and configuration
├── test_conversation_flows.py           # TC-CF-001 to TC-CF-004
├── test_multilingual_support.py         # TC-ML-001 to TC-ML-003
├── test_appointment_management.py       # TC-AM-001 to TC-AM-005
└── test_edge_cases.py                   # TC-EC-001 to TC-EC-006
```

## Running Tests

### Run all tests
```bash
pytest
```

### Run specific test file
```bash
pytest tests/test_conversation_flows.py
pytest tests/test_multilingual_support.py
pytest tests/test_appointment_management.py
pytest tests/test_edge_cases.py
```

### Run tests by marker
```bash
# Integration tests only
pytest -m integration

# Multilingual tests only
pytest -m multilingual

# Edge case tests only
pytest -m edge_case
```

### Run specific test class or function
```bash
# Run specific class
pytest tests/test_conversation_flows.py::TestInitialContactAndWelcome

# Run specific test
pytest tests/test_conversation_flows.py::TestInitialContactAndWelcome::test_welcome_message_japanese
```

### Run with coverage
```bash
pytest --cov=clinic_ai --cov-report=html
```

### Run with verbose output
```bash
pytest -v
pytest -vv  # Extra verbose
```

## Test Categories

### 1. Conversation Flow Tests (`test_conversation_flows.py`)

**Coverage**: TC-CF-001 to TC-CF-004

Tests for:
- Initial contact and welcome messages (Japanese, Chinese)
- Information collection workflows
- Price inquiry handling
- Appointment confirmation processes

**Key Tests**:
- `test_welcome_message_japanese()` - Welcome message for Japanese users
- `test_welcome_message_chinese()` - Welcome message for Chinese users
- `test_validates_required_fields()` - Data validation
- `test_handles_price_inquiry()` - Price inquiry responses
- `test_appointment_booking_complete_flow()` - End-to-end booking

### 2. Multilingual Support Tests (`test_multilingual_support.py`)

**Coverage**: TC-ML-001 to TC-ML-003

Tests for:
- Japanese language processing and intent recognition
- Chinese (Traditional) language processing
- Medical terminology translation across 4 languages
- Language detection accuracy

**Key Tests**:
- `test_intent_nose_consultation_request()` - Japanese intent classification
- `test_intent_consultation_process_inquiry()` - Chinese intent classification
- `test_medical_term_translation()` - Medical terminology accuracy (parameterized)
- `test_language_detection_accuracy()` - Language detection (parameterized)

**Supported Languages**: Korean (ko), Japanese (ja), Chinese (zh), English (en)

### 3. Appointment Management Tests (`test_appointment_management.py`)

**Coverage**: TC-AM-001 to TC-AM-005

Tests for:
- Date availability checking
- Appointment time changes
- Multi-person group bookings
- Pre-appointment reminders
- Returning customer recognition

**Key Tests**:
- `test_date_fully_booked()` - Fully booked date handling
- `test_date_partially_available()` - Split slot allocation
- `test_time_change_request_accepted()` - Time change workflow
- `test_split_group_into_different_slots()` - Group booking optimization
- `test_reminder_sent_1_to_3_days_before()` - Reminder timing
- `test_identifies_returning_customer()` - Customer history recognition

### 4. Edge Case Tests (`test_edge_cases.py`)

**Coverage**: TC-EC-001 to TC-EC-006

Tests for:
- Off-hours auto-reply
- Last-minute delay notifications
- Incomplete information handling
- Language barriers and interpreter needs
- Product/service unavailability
- Duplicate message handling

**Key Tests**:
- `test_business_hours_detection()` - Business hours accuracy (parameterized)
- `test_off_hours_auto_reply_chinese()` - Auto-reply in Chinese
- `test_delay_notification_acknowledged()` - Delay handling
- `test_identifies_missing_required_fields()` - Data validation
- `test_handles_interpreter_concern()` - Interpreter availability
- `test_detects_duplicate_messages()` - Duplicate detection

## Fixtures

All fixtures are defined in `conftest.py`:

### Customer Personas
- `japanese_customer_persona` - Based on real Japanese customer (NAK*********)
- `chinese_customer_persona` - Based on real Taiwanese customer (Huang ****)

### Appointment Fixtures
- `single_appointment` - Single person appointment
- `group_appointment` - Multi-person appointment
- `appointment_with_time_change` - Rescheduled appointment

### Calendar Fixtures
- `calendar_fully_booked` - All slots booked
- `calendar_partially_available` - Some slots available
- `calendar_fully_available` - All slots free

### Message Fixtures
- `price_inquiry_messages` - Price-related inquiries
- `consultation_request_messages` - Consultation requests
- `delay_notification_messages` - Delay notifications

### Service Fixtures
- `medical_terms` - Medical terminology in 4 languages
- `business_hours` - Operating hours configuration
- `pricing_info` - Service pricing information

### Mock Services
- `mock_translation_service` - Translation API mock
- `mock_ai_service` - AI service mock
- `mock_calendar_service` - Calendar service mock

## Test Coverage Goals

| Component | Target Coverage | Current Status |
|-----------|-----------------|----------------|
| Conversation Flows | 90% | ⚠️ Needs implementation |
| Multilingual Support | 95% | ⚠️ Needs implementation |
| Appointment Management | 90% | ⚠️ Needs implementation |
| Edge Cases | 85% | ⚠️ Needs implementation |
| **Overall** | **85-95%** | **⚠️ In Progress** |

## Real Customer Scenarios Tested

### Japanese Customer Journey (NAK*********)
- Initial inquiry about nose consultation
- Cannot bring interpreter
- Requests time change (17:00 → 14:00)
- Confirms attendance
- Completes consultation

**Tests**: `test_complete_japanese_booking_flow()`

### Chinese Customer Journey (Huang ****)
- Multiple price inquiries
- Group booking (3 people)
- Language support questions
- Last-minute delay (metro card issue)
- Returning customer (2nd visit after 8 months)

**Tests**: `test_complete_chinese_multi_person_booking_flow()`

## Parametrized Tests

Several tests use `@pytest.mark.parametrize` for comprehensive coverage:

- `test_medical_term_translation()` - 10+ translation pairs
- `test_language_detection_accuracy()` - 8 language samples
- `test_business_hours_detection()` - 7 time scenarios

## Test Markers

Use markers to filter tests:

```python
@pytest.mark.integration
@pytest.mark.multilingual
@pytest.mark.appointment
@pytest.mark.conversation
@pytest.mark.edge_case
@pytest.mark.slow
```

## Writing New Tests

### 1. Follow existing patterns

```python
class TestNewFeature:
    """TC-XX-001: New Feature Description"""

    def test_specific_scenario(self):
        """Test description"""
        # Given
        input_data = {...}

        # When
        result = self._method_under_test(input_data)

        # Then
        assert result["expected_field"] == expected_value
```

### 2. Use fixtures

```python
def test_with_fixture(japanese_customer_persona):
    assert japanese_customer_persona["language"] == "ja"
```

### 3. Add helper methods

```python
def _helper_method(self, data):
    """Helper to perform specific operation"""
    # Implementation
    return result
```

### 4. Document test cases

- Reference test case ID (TC-XX-NNN)
- Include clear description
- Use Given-When-Then structure

## Continuous Integration

Tests can be integrated into CI/CD pipeline:

```yaml
# .github/workflows/tests.yml
- name: Run tests
  run: |
    pytest --cov=clinic_ai --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
```

## Dependencies

Required packages for running tests:

```bash
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-mock>=3.10.0
pytest-django>=4.5.0  # If using Django
pytest-xdist>=3.0.0   # For parallel execution
```

Install test dependencies:

```bash
pip install -r requirements-test.txt
```

## Troubleshooting

### Tests failing due to imports

Make sure Django is properly configured:
```bash
export DJANGO_SETTINGS_MODULE=config.settings
```

### Slow test execution

Run tests in parallel:
```bash
pytest -n auto
```

### Coverage not showing

Install pytest-cov:
```bash
pip install pytest-cov
```

## Next Steps

1. **Implement actual services** - Replace helper methods with real implementations
2. **Add integration tests** - Test real API calls and database operations
3. **Add performance tests** - Test response time targets (<2 seconds)
4. **Add E2E tests** - Test complete user journeys with real messaging platforms
5. **Set up CI/CD** - Automate test execution on every commit

## Related Documentation

- [Test Cases](../sample_data/test_cases.md) - Detailed test case specifications
- [Sample Chat Logs](../sample_data/) - Real customer conversation data
- [Architecture](../README.md) - System architecture overview

## Questions?

For questions about tests, please refer to:
- Test case documentation in `sample_data/test_cases.md`
- Sample customer conversations in `sample_data/`
- Project README at root level
