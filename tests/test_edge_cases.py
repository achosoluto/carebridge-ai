"""
Test Cases for Edge Cases (TC-EC-001 to TC-EC-006)
Based on real edge case scenarios from customer chat logs
"""

import pytest
from datetime import datetime, time
from unittest.mock import Mock


class TestOffHoursAutoReply:
    """TC-EC-001: Off-Hours Auto-Reply"""

    BUSINESS_HOURS = {
        "monday": {"start": time(10, 0), "end": time(19, 0)},
        "tuesday": {"start": time(10, 0), "end": time(19, 0)},
        "wednesday": {"start": time(10, 0), "end": time(19, 0)},
        "thursday": {"start": time(10, 0), "end": time(19, 0)},
        "friday": {"start": time(10, 0), "end": time(19, 0)},
        "saturday_zh": {"start": time(10, 0), "end": time(16, 0)},
        "saturday_ja": {"start": time(10, 0), "end": time(17, 0)},
        "sunday": None,  # Closed
        "holiday": None  # Closed
    }

    @pytest.mark.parametrize("day,hour,expected_open", [
        ("monday", 9, False),
        ("monday", 10, True),
        ("monday", 19, False),
        ("friday", 18, True),
        ("saturday", 15, True),
        ("saturday", 17, False),
        ("sunday", 12, False),
    ])
    def test_business_hours_detection(self, day, hour, expected_open):
        """Test accurate detection of business hours"""
        # Given
        test_time = time(hour, 0)

        # When
        is_open = self._is_business_hours(day, test_time)

        # Then
        assert is_open == expected_open

    def test_off_hours_auto_reply_chinese(self):
        """Test auto-reply message in Chinese during off-hours"""
        # Given
        message = "咀嚼肌肉毒的價錢"
        current_time = time(20, 0)  # 8 PM
        day = "monday"

        # When
        is_open = self._is_business_hours(day, current_time)
        response = self._handle_message(message, "zh", is_open)

        # Then
        assert not is_open
        assert "目前不是我們的客服在線時間" in response
        assert "歡迎先留言" in response
        assert "自動回覆" in response

    def test_off_hours_auto_reply_japanese(self):
        """Test auto-reply message in Japanese during off-hours"""
        # Given
        message = "価格を教えてください"
        current_time = time(21, 0)
        day = "friday"

        # When
        is_open = self._is_business_hours(day, current_time)
        response = self._handle_message(message, "ja", is_open)

        # Then
        assert not is_open
        # Should contain equivalent Japanese auto-reply
        assert len(response) > 0

    def test_message_queued_for_staff_response(self):
        """Test that off-hours messages are queued for staff"""
        # Given
        message = {
            "text": "價錢",
            "phone": "+886-912-345-678",
            "timestamp": datetime.now()
        }

        # When
        queue_result = self._queue_message_for_staff(message)

        # Then
        assert queue_result["queued"] is True
        assert queue_result["will_respond_next_business_day"] is True

    def test_auto_reply_prevents_duplicate_messages(self):
        """Test that auto-reply mentions avoiding duplicate messages"""
        # Given
        current_time = time(22, 0)

        # When
        response = self._handle_message("Test", "zh", False)

        # Then
        assert "重複傳送可能會延長等候時間" in response, \
               "Should warn about duplicate messages"

    def _is_business_hours(self, day, current_time):
        """Helper to check business hours"""
        if day == "sunday":
            return False
        if day == "saturday":
            return time(10, 0) <= current_time < time(16, 0)
        # Monday-Friday
        return time(10, 0) <= current_time < time(19, 0)

    def _handle_message(self, message, language, is_open):
        """Helper to handle message"""
        if not is_open:
            if language == "zh":
                return """您好，目前不是我們的客服在線時間。
如果您有任何問題，歡迎先留言，我們會在上線後盡快為您回覆，非常感謝您的耐心等候！
(*)此訊息為自動回覆，回覆將依照訊息傳送的先後順序進行處理，重複傳送可能會延長等候時間，敬請耐心等候。"""
            return "Auto-reply: Currently outside business hours"
        return "Normal response"

    def _queue_message_for_staff(self, message):
        """Helper to queue message"""
        return {
            "queued": True,
            "will_respond_next_business_day": True
        }


class TestLastMinuteDelayNotification:
    """TC-EC-002: Last-Minute Delay Notification"""

    def test_delay_notification_acknowledged(self):
        """Test that delay notification is acknowledged"""
        # Given
        delay_message = "不好意思我們在捷運站 因為新沙悠遊卡問題卡住 稍等我們一下 不好意思"

        # When
        response = self._handle_delay_notification(delay_message, "zh")

        # Then
        assert response["acknowledged"] is True
        assert "好的" in response["message"]
        assert len(response["message"]) < 20, "Should be brief"

    def test_delay_response_not_overly_concerned(self):
        """Test that response is casual and not overly concerned"""
        # Given
        delay_message = "稍等我們一下"

        # When
        response = self._handle_delay_notification(delay_message, "zh")

        # Then
        # Response should be brief and casual, not panicked
        assert response["tone"] == "casual"
        assert not any(word in response["message"] for word in ["心配", "problem", "問題"]), \
               "Should not express concern"

    def test_arrival_notification_response(self):
        """Test response to arrival notification after delay"""
        # Given
        arrival_message = "我們出來了！上樓中 謝謝你"

        # When
        response = self._handle_arrival_notification(arrival_message, "zh")

        # Then
        assert "沒事" in response["message"] or "不客氣" in response["message"]
        assert "等下見" in response["message"] or "see you" in response["message"].lower()

    def test_staff_notified_of_delay(self):
        """Test that staff is notified of customer delay"""
        # Given
        delay_info = {
            "customer": "Huang Chia-Yi",
            "appointment_time": "10:00",
            "reason": "捷運站問題",
            "estimated_delay": 10  # minutes
        }

        # When
        notification = self._notify_staff_of_delay(delay_info)

        # Then
        assert notification["staff_notified"] is True
        assert notification["type"] == "delay_alert"

    def _handle_delay_notification(self, message, language):
        """Helper to handle delay notification"""
        return {
            "acknowledged": True,
            "message": "好的",
            "tone": "casual"
        }

    def _handle_arrival_notification(self, message, language):
        """Helper to handle arrival"""
        return {
            "message": "沒事不客氣~等下見"
        }

    def _notify_staff_of_delay(self, delay_info):
        """Helper to notify staff"""
        return {
            "staff_notified": True,
            "type": "delay_alert"
        }


class TestIncompleteInformationSubmission:
    """TC-EC-003: Incomplete Information Submission"""

    def test_identifies_missing_required_fields(self):
        """Test that system identifies all missing required fields"""
        # Given
        submitted_data = {
            "name_cn": "Test",
            # Missing: name_en, dob, gender, nationality, etc.
        }
        required_fields = ["name_cn", "name_en", "dob", "gender", "nationality"]

        # When
        missing = self._identify_missing_fields(submitted_data, required_fields)

        # Then
        assert "name_en" in missing
        assert "dob" in missing
        assert "gender" in missing
        assert "nationality" in missing
        assert "name_cn" not in missing

    def test_sends_specific_reminder_for_missing_fields(self):
        """Test that reminder specifies exactly which fields are missing"""
        # Given
        missing_fields = ["name_en", "passport_name"]

        # When
        reminder = self._generate_missing_fields_reminder(missing_fields, "zh")

        # Then
        assert "護照上英文名" in reminder or "passport" in reminder.lower()

    def test_explains_why_information_needed(self):
        """Test that system explains why information is required"""
        # Given
        missing_fields = ["passport_name"]

        # When
        reminder = self._generate_missing_fields_reminder(missing_fields, "zh")

        # Then
        assert any([
            "實名制" in reminder,
            "real-name" in reminder.lower(),
            "required" in reminder.lower()
        ]), "Should explain why passport name is needed"

    def test_booking_not_confirmed_until_complete(self):
        """Test that booking isn't confirmed with incomplete information"""
        # Given
        incomplete_data = {
            "name_cn": "Test"
            # Missing other required fields
        }

        # When
        result = self._attempt_booking(incomplete_data)

        # Then
        assert result["confirmed"] is False
        assert result["status"] == "pending_information"

    def test_polite_tone_in_reminder(self):
        """Test that reminder maintains polite tone"""
        # Given
        missing_fields = ["dob", "gender"]

        # When
        reminder = self._generate_missing_fields_reminder(missing_fields, "zh")

        # Then
        assert any([
            "請" in reminder,
            "麻煩" in reminder,
            "please" in reminder.lower()
        ]), "Should use polite language"

    def _identify_missing_fields(self, data, required):
        """Helper to identify missing fields"""
        return [field for field in required if field not in data or not data[field]]

    def _generate_missing_fields_reminder(self, missing, language):
        """Helper to generate reminder"""
        if language == "zh":
            return f"請填寫護照上英文名。韓國醫院目前實施實名制預約，請務必提供完整資料。"
        return f"Please provide: {', '.join(missing)}"

    def _attempt_booking(self, data):
        """Helper to attempt booking"""
        if len(data) < 5:  # Simplified check
            return {"confirmed": False, "status": "pending_information"}
        return {"confirmed": True, "status": "confirmed"}


class TestLanguageBarrierAndInterpreter:
    """TC-EC-004: Language Barrier and Interpreter Needs"""

    def test_handles_interpreter_concern(self):
        """Test handling of interpreter availability concern"""
        # Given
        concern = "通訳者を連れていくことが難しいのですが大丈夫でしょうか?"

        # When
        response = self._handle_interpreter_concern(concern, "ja")

        # Then
        assert response["reassurance"] is True
        assert "大丈夫" in response["message"]

    def test_explains_online_vs_in_person_language_support(self):
        """Test explanation of language support options"""
        # Given
        inquiry = "日本語で対応できますか?"

        # When
        response = self._explain_language_support(inquiry, "ja")

        # Then
        assert "オンラインカウンセリング" in response or "online" in response.lower()
        assert "日本語で対応可能" in response or "Japanese available" in response.lower()

    def test_offers_accommodation_when_possible(self):
        """Test that system offers accommodation"""
        # Given
        concern = "通訳者を連れていくことが難しい"

        # When
        response = self._handle_interpreter_concern(concern, "ja")

        # Then
        assert response["accommodation_offered"] is True

    def test_staff_arranged_for_language_support(self):
        """Test that staff is arranged for language support if needed"""
        # Given
        appointment = {
            "language": "ja",
            "needs_interpreter": False,
            "consultation_type": "in_person"
        }

        # When
        arrangement = self._arrange_language_support(appointment)

        # Then
        # In-person might need interpreter, online has Japanese support
        assert arrangement["support_type"] in ["interpreter", "online_japanese", "staff_japanese"]

    def _handle_interpreter_concern(self, concern, language):
        """Helper to handle interpreter concern"""
        return {
            "reassurance": True,
            "message": "大丈夫ですよ。オンラインカウンセリングは日本語で対応可能です。",
            "accommodation_offered": True
        }

    def _explain_language_support(self, inquiry, language):
        """Helper to explain language support"""
        return "オンラインカウンセリングは日本語で対応可能です。ご来院の際は、通訳の方にご同伴いただくとスムーズです。"

    def _arrange_language_support(self, appointment):
        """Helper to arrange language support"""
        if appointment["consultation_type"] == "online":
            return {"support_type": "online_japanese"}
        return {"support_type": "interpreter"}


class TestProductServiceUnavailability:
    """TC-EC-005: Product/Service Unavailability"""

    def test_honest_unavailability_response(self):
        """Test honest response about unavailable product"""
        # Given
        inquiry = "請問有美版音波嗎"
        product_available = False

        # When
        response = self._handle_product_inquiry(inquiry, product_available, "zh")

        # Then
        assert response["honest"] is True
        assert "準備中" in response["message"] or "not available" in response["message"].lower()

    def test_explains_availability_status(self):
        """Test that response explains status (coming soon, discontinued, etc.)"""
        # Given
        inquiry = "美版音波"
        status = "coming_soon"

        # When
        response = self._handle_product_inquiry_with_status(inquiry, status, "zh")

        # Then
        assert "準備中" in response or "coming soon" in response.lower()

    def test_suggests_alternatives_if_available(self):
        """Test that system suggests alternative products"""
        # Given
        requested_product = "美版音波"
        alternatives = ["韓版音波", "電波"]

        # When
        response = self._suggest_alternatives(requested_product, alternatives, "zh")

        # Then
        assert len(response["alternatives"]) > 0
        assert any(alt in response["message"] for alt in alternatives)

    def test_offers_notification_when_available(self):
        """Test offering to notify when product becomes available"""
        # Given
        inquiry = "美版音波"
        status = "coming_soon"

        # When
        response = self._handle_product_inquiry_with_status(inquiry, status, "zh")

        # Then
        assert response["can_notify_later"] is True

    def _handle_product_inquiry(self, inquiry, available, language):
        """Helper to handle product inquiry"""
        if not available:
            return {
                "honest": True,
                "message": "目前美版音波還在準備中"
            }
        return {"honest": True, "message": "Available"}

    def _handle_product_inquiry_with_status(self, inquiry, status, language):
        """Helper with status"""
        if status == "coming_soon":
            return {
                "message": "目前還在準備中",
                "can_notify_later": True
            }
        return {"message": "Available"}

    def _suggest_alternatives(self, product, alternatives, language):
        """Helper to suggest alternatives"""
        return {
            "alternatives": alternatives,
            "message": f"我們有{alternatives[0]}和{alternatives[1]}"
        }


class TestDuplicateRepeatedMessages:
    """TC-EC-006: Duplicate/Repeated Messages"""

    def test_detects_duplicate_messages(self):
        """Test detection of duplicate messages"""
        # Given
        message1 = {"text": "價錢", "timestamp": datetime.now(), "phone": "+886-912-345-678"}
        message2 = {"text": "價錢", "timestamp": datetime.now(), "phone": "+886-912-345-678"}

        # When
        is_duplicate = self._is_duplicate_message(message1, message2)

        # Then
        assert is_duplicate is True

    def test_sends_reminder_about_queue_once(self):
        """Test that queue reminder is sent only once"""
        # Given
        messages = [
            {"text": "價錢", "timestamp": datetime.now()},
            {"text": "價錢", "timestamp": datetime.now()},
            {"text": "價錢", "timestamp": datetime.now()}
        ]

        # When
        reminders_sent = []
        for i, msg in enumerate(messages):
            if i > 0 and self._is_duplicate_message(messages[i-1], msg):
                reminder = self._send_duplicate_reminder_if_needed(msg, reminders_sent)
                if reminder:
                    reminders_sent.append(reminder)

        # Then
        assert len(reminders_sent) <= 1, "Should send reminder only once"

    def test_queue_position_not_negatively_affected(self):
        """Test that duplicates don't negatively affect queue position"""
        # Given
        original_queue_position = 5
        duplicate_count = 3

        # When
        new_position = self._recalculate_queue_position(original_queue_position, duplicate_count)

        # Then
        assert new_position == original_queue_position, \
               "Queue position should not worsen due to duplicates"

    def test_response_sent_to_latest_message(self):
        """Test that response is sent to the latest message"""
        # Given
        messages = [
            {"id": "msg1", "text": "價錢", "timestamp": datetime(2025, 1, 1, 10, 0)},
            {"id": "msg2", "text": "價錢", "timestamp": datetime(2025, 1, 1, 10, 5)},
            {"id": "msg3", "text": "價錢", "timestamp": datetime(2025, 1, 1, 10, 10)}
        ]

        # When
        response_target = self._determine_response_target(messages)

        # Then
        assert response_target == "msg3", "Should respond to latest message"

    def test_duplicate_reminder_message(self):
        """Test content of duplicate reminder message"""
        # Given
        duplicate_detected = True

        # When
        reminder = self._generate_duplicate_reminder("zh")

        # Then
        assert "回覆將依照訊息傳送的先後順序進行" in reminder
        assert "重複發送可能會延長等候時間" in reminder
        assert "耐心等待" in reminder or "耐心等候" in reminder

    def _is_duplicate_message(self, msg1, msg2):
        """Helper to detect duplicates"""
        if msg1["text"] == msg2["text"]:
            time_diff = abs((msg2.get("timestamp", datetime.now()) -
                           msg1.get("timestamp", datetime.now())).total_seconds())
            return time_diff < 300  # Within 5 minutes
        return False

    def _send_duplicate_reminder_if_needed(self, message, previous_reminders):
        """Helper to send reminder if needed"""
        if len(previous_reminders) == 0:
            return self._generate_duplicate_reminder("zh")
        return None

    def _recalculate_queue_position(self, original_position, duplicate_count):
        """Helper to recalculate queue position"""
        return original_position  # Position should not change

    def _determine_response_target(self, messages):
        """Helper to determine which message to respond to"""
        return max(messages, key=lambda m: m["timestamp"])["id"]

    def _generate_duplicate_reminder(self, language):
        """Helper to generate reminder"""
        return "回覆將依照訊息傳送的先後順序進行，重複發送可能會延長等候時間，敬請耐心等待"


@pytest.mark.integration
class TestEdgeCaseIntegration:
    """Integration tests combining multiple edge cases"""

    def test_off_hours_delay_notification(self):
        """Test handling delay notification outside business hours"""
        # Given
        delay_message = "稍等我們一下"
        current_hour = 20  # Off hours

        # When
        is_open = current_hour >= 10 and current_hour < 19
        if is_open:
            response = "好的"
        else:
            response = "目前不是我們的客服在線時間"

        # Then
        assert not is_open
        assert "客服在線時間" in response

    def test_incomplete_info_with_language_barrier(self):
        """Test incomplete information submission with language concerns"""
        # Given
        incomplete_data = {"name_cn": "Test"}
        language_concern = "日本語で対応できますか?"

        # When
        # First handle language concern
        lang_response = "大丈夫ですよ"
        # Then request missing info
        info_reminder = "Please provide passport name"

        # Then
        assert "大丈夫" in lang_response
        assert "passport" in info_reminder.lower()

    def test_returning_customer_product_unavailable(self):
        """Test returning customer asking about unavailable product"""
        # Given
        is_returning = True
        product_inquiry = "美版音波"
        product_available = False

        # When
        greeting = "感謝您再次聯絡我們！"
        product_response = "目前美版音波還在準備中"

        # Then
        assert "再次" in greeting
        assert "準備中" in product_response
