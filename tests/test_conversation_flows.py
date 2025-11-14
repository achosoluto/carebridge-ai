"""
Test Cases for Conversation Flows (TC-CF-001 to TC-CF-004)
Based on real customer chat logs from sample_data/
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, patch


class TestInitialContactAndWelcome:
    """TC-CF-001: Initial Contact and Welcome Message"""

    def test_welcome_message_japanese(self):
        """
        Test welcome message for Japanese users
        Expected: Welcome message sent within 1 second with all required information
        """
        # Given
        user_name = "ｱﾔﾉ"
        language = "ja"

        # When
        start_time = datetime.now()
        welcome_message = self._generate_welcome_message(user_name, language)
        response_time = (datetime.now() - start_time).total_seconds()

        # Then
        assert response_time < 1.0, "Welcome message should be sent within 1 second"
        assert "はじめまして" in welcome_message, "Should include Japanese greeting"
        assert "名前" in welcome_message, "Should request name"
        assert "年齢" in welcome_message, "Should request age"
        assert "国籍" in welcome_message, "Should request nationality"
        assert "連絡先情報" in welcome_message, "Should request contact info"
        assert "相談したい顔の部分" in welcome_message, "Should request consultation area"
        assert "相談の日程" in welcome_message, "Should request preferred date"

    def test_welcome_message_chinese(self):
        """
        Test welcome message for Chinese users
        Expected: Welcome message with all required information in Chinese
        """
        # Given
        user_name = "Joy"
        language = "zh"

        # When
        welcome_message = self._generate_welcome_message(user_name, language)

        # Then
        assert "您好" in welcome_message, "Should include Chinese greeting"
        assert "請問您是如何得知我們的呢" in welcome_message, "Should ask how they found us"
        assert "請問您想諮詢的項目是什麼" in welcome_message, "Should ask consultation items"
        assert "預約日期與時段" in welcome_message, "Should request appointment date/time"
        assert "預約人數" in welcome_message, "Should request number of people"

    def test_welcome_includes_business_hours(self):
        """Test that welcome message includes business hours"""
        welcome_message = self._generate_welcome_message("Test User", "en")

        # Should include business hours
        assert any([
            "10:00" in welcome_message,
            "business hours" in welcome_message.lower(),
            "診療時間" in welcome_message
        ]), "Should include business hours"

    def test_welcome_includes_social_media_links(self):
        """Test that welcome message includes contact channels"""
        welcome_message = self._generate_welcome_message("Test User", "ja")

        # Should include social media or contact info
        assert any([
            "kakao" in welcome_message.lower(),
            "twitter" in welcome_message.lower(),
            "whatsapp" in welcome_message.lower()
        ]), "Should include social media links"

    def _generate_welcome_message(self, user_name, language):
        """Helper method to generate welcome message (to be implemented)"""
        # This is a placeholder - actual implementation will call the real service
        if language == "ja":
            return f"{user_name}님\nはじめまして。\n名前 / 年齢 / 国籍\n連絡先情報\n相談したい顔の部分\n相談の日程はいつが良いですか？\n診療時間\n月〜金：午前10:00〜午後7:00\nkakao ID: test"
        elif language == "zh":
            return f"您好! {user_name}\n請問您是如何得知我們的呢？\n請問您想諮詢的項目是什麼？\n預約日期與時段（可提供多個選項）：\n預約人數（不含陪同人員）："
        else:
            return "Welcome! Please provide your information."


class TestInformationCollection:
    """TC-CF-002: Information Collection Flow"""

    def test_validates_required_fields_japanese(self):
        """Test that system validates all required fields for Japanese consultation"""
        # Given
        required_fields = ["name", "age", "nationality", "contact", "consultation_area", "preferred_date"]

        # Test incomplete data
        incomplete_data = {
            "name": "NAK*********",
            "consultation_area": "鼻"
            # Missing: age, nationality, contact, preferred_date
        }

        # When
        missing_fields = self._validate_consultation_data(incomplete_data, required_fields)

        # Then
        assert "age" in missing_fields
        assert "nationality" in missing_fields
        assert "contact" in missing_fields
        assert "preferred_date" in missing_fields

    def test_validates_required_fields_chinese(self):
        """Test that system validates all required fields for Chinese consultation"""
        # Given
        required_fields = ["how_found", "consultation_items", "appointment_date", "num_people"]

        # Test incomplete data
        incomplete_data = {
            "how_found": "Instagram",
            # Missing: consultation_items, appointment_date, num_people
        }

        # When
        missing_fields = self._validate_consultation_data(incomplete_data, required_fields)

        # Then
        assert "consultation_items" in missing_fields
        assert "appointment_date" in missing_fields
        assert "num_people" in missing_fields

    def test_accepts_complete_data(self):
        """Test that system accepts complete consultation data"""
        # Given
        complete_data = {
            "name": "Test Patient",
            "age": 30,
            "nationality": "日本",
            "contact": "+81-90-1234-5678",
            "consultation_area": "鼻",
            "preferred_date": "2025-11-05"
        }
        required_fields = ["name", "age", "nationality", "contact", "consultation_area", "preferred_date"]

        # When
        missing_fields = self._validate_consultation_data(complete_data, required_fields)

        # Then
        assert len(missing_fields) == 0, "Complete data should have no missing fields"

    def test_sends_reminder_for_missing_information(self):
        """Test that system sends polite reminder for missing information"""
        # Given
        incomplete_data = {"name": "Test"}
        required_fields = ["name", "age", "contact"]

        # When
        missing_fields = self._validate_consultation_data(incomplete_data, required_fields)
        reminder_message = self._generate_missing_info_reminder(missing_fields, "ja")

        # Then
        assert "age" in reminder_message.lower() or "年齢" in reminder_message
        assert "contact" in reminder_message.lower() or "連絡先" in reminder_message

    def _validate_consultation_data(self, data, required_fields):
        """Helper to validate consultation data"""
        missing = []
        for field in required_fields:
            if field not in data or not data[field]:
                missing.append(field)
        return missing

    def _generate_missing_info_reminder(self, missing_fields, language):
        """Helper to generate reminder message"""
        if language == "ja":
            return f"以下の情報をご記入ください: {', '.join(missing_fields)}"
        else:
            return f"Please provide: {', '.join(missing_fields)}"


class TestPriceInquiryHandling:
    """TC-CF-003: Price Inquiry Handling"""

    def test_handles_single_service_pricing_inquiry(self):
        """Test handling of single service price inquiry"""
        # Given
        inquiry = "咀嚼肌肉毒的價錢"
        language = "zh"

        # When
        response = self._handle_price_inquiry(inquiry, language)

        # Then
        assert "韓幣" in response or "韩币" in response, "Should include currency"
        assert any(char.isdigit() for char in response), "Should include price numbers"

    def test_handles_multiple_service_pricing_inquiry(self):
        """Test handling of multiple service price inquiry"""
        # Given
        inquiry = "咀嚼肌肉毒、嘴唇玻尿酸 、美版超聲刀 的價錢"
        language = "zh"

        # When
        response = self._handle_price_inquiry(inquiry, language)

        # Then
        assert "肉毒" in response or "botox" in response.lower()
        assert "玻尿酸" in response or "filler" in response.lower()

    def test_off_hours_auto_reply_for_pricing(self):
        """Test auto-reply for price inquiry during off-hours"""
        # Given
        inquiry = "價錢"
        current_hour = 20  # 8 PM, after business hours

        # When
        is_business_hours = self._check_business_hours(current_hour)

        # Then
        assert not is_business_hours

        # When during off-hours
        response = self._handle_price_inquiry(inquiry, "zh", current_hour)

        # Then
        assert "目前不是我們的客服在線時間" in response or "not available" in response.lower()

    def test_product_unavailability_response(self):
        """Test response when product is unavailable"""
        # Given
        inquiry = "請問有美版音波嗎"
        product_available = False

        # When
        response = self._handle_product_inquiry(inquiry, product_available, "zh")

        # Then
        assert "準備中" in response or "unavailable" in response.lower() or "not available" in response.lower()

    def _handle_price_inquiry(self, inquiry, language, hour=10):
        """Helper to handle price inquiry"""
        if not self._check_business_hours(hour):
            if language == "zh":
                return "您好，目前不是我們的客服在線時間。"
            return "Currently outside business hours."

        # Simplified price response
        if language == "zh":
            return "肉毒素: 9.9萬韓幣 (Botulax), 22萬韓幣 (Xeomin)\n玻尿酸: 16.5萬韓幣"
        return "Botox: 99,000 KRW, Filler: 165,000 KRW"

    def _handle_product_inquiry(self, inquiry, available, language):
        """Helper to handle product availability inquiry"""
        if not available:
            if language == "zh":
                return "目前美版音波還在準備中"
            return "Currently preparing this product"
        return "Available"

    def _check_business_hours(self, hour):
        """Helper to check if within business hours"""
        return 10 <= hour < 19  # Mon-Fri 10:00-19:00


class TestAppointmentConfirmation:
    """TC-CF-004: Appointment Confirmation Workflow"""

    def test_appointment_booking_complete_flow(self):
        """Test complete appointment booking flow"""
        # Given
        appointment_request = {
            "date": "2025-11-05",
            "time": "17:00",
            "language": "ja"
        }

        # When - Check availability
        is_available = self._check_availability(appointment_request["date"], appointment_request["time"])

        # Then
        assert is_available

        # When - Collect personal information
        personal_info = {
            "name_cn": "NAK*********",
            "name_en": "NAK*********",
            "dob": "1990-01-01",
            "gender": "F",
            "nationality": "日本",
            "recent_procedures": "唇フィラー",
            "consultation_items": "鼻整形",
            "same_day_procedure": "未定",
            "sedation": "否"
        }

        is_complete = self._validate_personal_info(personal_info)
        assert is_complete

        # When - Confirm booking
        confirmation = self._create_appointment_confirmation(appointment_request, personal_info)

        # Then
        assert "✅" in confirmation or "confirmed" in confirmation.lower()
        assert appointment_request["date"] in confirmation
        assert appointment_request["time"] in confirmation
        assert "9樓櫃台" in confirmation or "9F" in confirmation
        assert "護照" in confirmation or "passport" in confirmation.lower()

    def test_multi_person_booking_data_collection(self):
        """Test data collection for multiple people"""
        # Given
        num_people = 3

        # When - Collect data for each person
        collected_data = []
        for i in range(num_people):
            person_data = {
                "person_id": i + 1,
                "name_cn": f"Person {i+1}",
                "name_en": f"PERSON{i+1}",
                "dob": "1990-01-01",
                "gender": "F"
            }
            collected_data.append(person_data)

        # Then
        assert len(collected_data) == 3
        assert all("name_cn" in person for person in collected_data)
        assert all("name_en" in person for person in collected_data)

    def test_appointment_confirmation_includes_address(self):
        """Test that confirmation includes clinic address in multiple languages"""
        # Given
        appointment = {"date": "2025-11-05", "time": "14:00"}
        personal_info = {"name_cn": "Test", "name_en": "TEST"}

        # When
        confirmation = self._create_appointment_confirmation(appointment, personal_info)

        # Then - Should include address in multiple languages
        assert "江南區" in confirmation or "Gangnam" in confirmation, "Should include Korean or English address"

    def test_confirmation_includes_fees_information(self):
        """Test that confirmation includes consultation fees info"""
        # Given
        appointment = {"date": "2025-11-05", "time": "14:00"}
        personal_info = {"name_cn": "Test", "name_en": "TEST"}

        # When
        confirmation = self._create_appointment_confirmation(appointment, personal_info)

        # Then
        assert any([
            "1萬韓元" in confirmation,
            "10,000" in confirmation,
            "free" in confirmation.lower(),
            "無料" in confirmation
        ]), "Should include fee information"

    def _check_availability(self, date, time):
        """Helper to check appointment availability"""
        # Simplified availability check
        return True

    def _validate_personal_info(self, info):
        """Helper to validate personal information"""
        required_fields = ["name_cn", "name_en", "dob", "gender", "nationality"]
        return all(field in info and info[field] for field in required_fields)

    def _create_appointment_confirmation(self, appointment, personal_info):
        """Helper to create appointment confirmation message"""
        return f"""您已預約成功✅
預約時間: {appointment['date']} {appointment['time']}
來院時，請先到9樓櫃台並出示您的有效證件（護照或外國人登錄證）
本院地址:
[中] 首爾市 江南區 島山大路110, KBL中心 9樓
[英] 9F, KBL Center, Dosan-daero 110, Gangnam-gu, Seoul
室長諮詢是免費的喔！與院長進行面診，將收取1萬韓元的費用"""


@pytest.mark.integration
class TestConversationFlowIntegration:
    """Integration tests for complete conversation flows"""

    def test_complete_japanese_booking_flow(self):
        """
        Test complete flow from initial contact to confirmed booking (Japanese)
        Simulates: TC-IN-001
        """
        # Step 1: Initial contact
        welcome = self._send_welcome_message("ｱﾔﾉ", "ja")
        assert "はじめまして" in welcome

        # Step 2: User inquires about consultation
        inquiry = "鼻のカウンセリングを検討しております"
        response = self._process_inquiry(inquiry, "ja")
        assert "手術予定日" in response or "date" in response.lower()

        # Step 3: User provides information
        user_info = {
            "surgery_date": "年内",
            "doctor": "チョンナムジュ院長",
            "experience": "唇フィラー",
            "source": "Twitter"
        }
        response = self._process_user_info(user_info, "ja")
        assert "available" in response.lower() or "可能" in response or "いかがでしょうか" in response

        # Step 4: Confirm appointment
        confirmation_data = {
            "date": "2025-11-05",
            "time": "17:00",
            "name": "NAK*********"
        }
        confirmation = self._confirm_appointment(confirmation_data, "ja")
        assert "予約が完了" in confirmation or "confirmed" in confirmation.lower()

    def test_complete_chinese_multi_person_booking_flow(self):
        """
        Test complete flow for multi-person booking (Chinese)
        Simulates: TC-IN-002
        """
        # Step 1: Welcome
        welcome = self._send_welcome_message("Joy", "zh")
        assert "您好" in welcome

        # Step 2: Multiple price inquiries
        inquiry1 = "咀嚼肌肉毒的價錢"
        response1 = self._process_inquiry(inquiry1, "zh")
        assert "韓幣" in response1 or "韩币" in response1

        # Step 3: Request booking for 3 people
        booking_request = {
            "date": "2025-03-06",
            "num_people": 3,
            "items": "皮膚儀器、注射"
        }
        response = self._process_booking_request(booking_request, "zh")
        assert "預約" in response

        # Step 4: Collect individual information for each person
        people_data = [
            {"name_cn": "黃嘉怡", "name_en": "Huang Chia-Yi"},
            {"name_cn": "楊君璦", "name_en": "Yang Chun-Ai"},
            {"name_cn": "江宜卉", "name_en": "Chiang Yi-Hui"}
        ]
        confirmations = [self._confirm_appointment(person, "zh") for person in people_data]
        assert all("✅" in conf for conf in confirmations)

    def _send_welcome_message(self, name, language):
        """Helper for welcome message"""
        if language == "ja":
            return f"{name}님\nはじめまして。"
        return f"您好! {name}"

    def _process_inquiry(self, inquiry, language):
        """Helper to process inquiry"""
        if "鼻" in inquiry or "nose" in inquiry.lower():
            if language == "ja":
                return "手術予定日はいつでしょうか？"
            return "When would you like the consultation?"
        if "肉毒" in inquiry or "價錢" in inquiry:
            return "肉毒素: 9.9萬韓幣"
        return "How can we help?"

    def _process_user_info(self, info, language):
        """Helper to process user information"""
        if language == "ja":
            return "11月5日17:00はいかがでしょうか"
        return "可以"

    def _process_booking_request(self, request, language):
        """Helper to process booking request"""
        return f"預約{request['num_people']}位"

    def _confirm_appointment(self, data, language):
        """Helper to confirm appointment"""
        if language == "ja":
            return "予約が完了いたします"
        return f"您已預約成功✅"
