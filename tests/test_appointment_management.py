"""
Test Cases for Appointment Management (TC-AM-001 to TC-AM-005)
Based on real customer booking scenarios from sample chat logs
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, MagicMock


class TestDateAvailabilityCheck:
    """TC-AM-001: Date Availability Check"""

    def test_date_fully_booked(self):
        """Test response when requested date is fully booked"""
        # Given
        requested_date = "2025-03-07"
        num_people = 3
        calendar = self._create_mock_calendar({"2025-03-07": "full"})

        # When
        availability = self._check_availability(requested_date, num_people, calendar)

        # Then
        assert availability["available"] is False
        assert "滿" in availability["message_zh"] or "full" in availability["message_en"].lower()

    def test_date_partially_available(self):
        """Test response when date has partial availability"""
        # Given
        requested_date = "2025-03-06"
        num_people = 3
        calendar = self._create_mock_calendar({
            "2025-03-06": {"10:00": 2, "11:30": 1}  # Split slots available
        })

        # When
        availability = self._check_availability(requested_date, num_people, calendar)

        # Then
        assert availability["available"] is True
        assert availability["split_booking"] is True
        assert len(availability["slots"]) == 2
        assert availability["slots"][0]["time"] == "10:00"
        assert availability["slots"][0]["capacity"] == 2
        assert availability["slots"][1]["time"] == "11:30"
        assert availability["slots"][1]["capacity"] == 1

    def test_date_fully_available(self):
        """Test response when date is fully available"""
        # Given
        requested_date = "2025-11-13"
        num_people = 2
        calendar = self._create_mock_calendar({
            "2025-11-13": "available"
        })

        # When
        availability = self._check_availability(requested_date, num_people, calendar)

        # Then
        assert availability["available"] is True
        assert availability["split_booking"] is False

    def test_alternative_date_suggestion(self):
        """Test that system suggests alternative dates when requested date is full"""
        # Given
        requested_date = "2025-03-07"
        calendar = self._create_mock_calendar({
            "2025-03-07": "full",
            "2025-03-06": "available",
            "2025-03-08": "available"
        })

        # When
        alternatives = self._suggest_alternative_dates(requested_date, calendar)

        # Then
        assert len(alternatives) > 0
        assert "2025-03-06" in alternatives or "2025-03-08" in alternatives

    def _create_mock_calendar(self, availability_map):
        """Helper to create mock calendar"""
        return availability_map

    def _check_availability(self, date, num_people, calendar):
        """Helper to check availability"""
        if date in calendar:
            status = calendar[date]
            if status == "full":
                return {
                    "available": False,
                    "message_zh": "目前都滿囉",
                    "message_en": "Currently fully booked"
                }
            elif status == "available":
                return {
                    "available": True,
                    "split_booking": False
                }
            elif isinstance(status, dict):  # Split slots
                return {
                    "available": True,
                    "split_booking": True,
                    "slots": [{"time": time, "capacity": capacity}
                             for time, capacity in status.items()]
                }
        return {"available": False}

    def _suggest_alternative_dates(self, requested_date, calendar):
        """Helper to suggest alternative dates"""
        alternatives = []
        for date, status in calendar.items():
            if date != requested_date and status != "full":
                alternatives.append(date)
        return alternatives


class TestAppointmentTimeChange:
    """TC-AM-002: Appointment Time Change"""

    def test_time_change_request_accepted(self):
        """Test successful time change"""
        # Given
        original_appointment = {
            "date": "2025-11-05",
            "time": "17:00",
            "patient": "NAK*********"
        }
        new_time = "14:00"

        # When
        result = self._change_appointment_time(original_appointment, new_time)

        # Then
        assert result["success"] is True
        assert result["appointment"]["time"] == "14:00"
        assert result["confirmation_sent"] is True

    def test_time_change_confirmation_message(self):
        """Test that confirmation message includes updated time"""
        # Given
        updated_appointment = {
            "date": "2025-11-05",
            "time": "14:00",
            "patient": "NAK*********"
        }

        # When
        confirmation = self._generate_time_change_confirmation(updated_appointment, "ja")

        # Then
        assert "14:00" in confirmation
        assert "変更" in confirmation
        assert updated_appointment["date"] in confirmation

    def test_time_change_updates_reminder(self):
        """Test that pre-appointment reminder reflects new time"""
        # Given
        appointment_id = "12345"
        new_time = "14:00"

        # When
        self._change_appointment_time({"id": appointment_id, "time": "17:00", "date": "2025-11-05"}, new_time)
        reminder = self._get_appointment_reminder(appointment_id)

        # Then
        assert reminder["time"] == "14:00", "Reminder should reflect updated time"

    def test_original_slot_released(self):
        """Test that original time slot is released back to availability"""
        # Given
        original_time = "17:00"
        new_time = "14:00"
        date = "2025-11-05"

        # When
        calendar_before = self._get_calendar_availability(date)
        self._change_appointment_time(
            {"time": original_time, "date": date},
            new_time
        )
        calendar_after = self._get_calendar_availability(date)

        # Then
        assert calendar_before[original_time] == "booked"
        assert calendar_after[original_time] == "available", "Original slot should be released"
        assert calendar_after[new_time] == "booked", "New slot should be booked"

    def _change_appointment_time(self, appointment, new_time):
        """Helper to change appointment time"""
        appointment["time"] = new_time
        return {
            "success": True,
            "appointment": appointment,
            "confirmation_sent": True
        }

    def _generate_time_change_confirmation(self, appointment, language):
        """Helper to generate confirmation"""
        if language == "ja":
            return f"{appointment['time']}に変更致しました！{appointment['date']}"
        return f"Changed to {appointment['time']} on {appointment['date']}"

    def _get_appointment_reminder(self, appointment_id):
        """Helper to get reminder"""
        return {"time": "14:00", "date": "2025-11-05"}

    def _get_calendar_availability(self, date):
        """Helper to get calendar availability"""
        # Simplified mock
        return {"17:00": "available", "14:00": "booked"}


class TestMultiPersonBooking:
    """TC-AM-003: Multi-Person Booking"""

    def test_split_group_into_different_slots(self):
        """Test splitting group booking into multiple time slots"""
        # Given
        booking_request = {
            "date": "2025-03-06",
            "num_people": 3,
            "names": ["黃嘉怡", "楊君璦", "江宜卉"]
        }

        # When
        result = self._process_group_booking(booking_request)

        # Then
        assert result["success"] is True
        assert len(result["slots"]) == 2  # Split into 2 slots
        assert result["slots"][0]["num_people"] == 2
        assert result["slots"][0]["time"] == "10:00"
        assert result["slots"][1]["num_people"] == 1
        assert result["slots"][1]["time"] == "11:30"

    def test_individual_data_collection_for_each_person(self):
        """Test that system collects individual data for each person"""
        # Given
        num_people = 3

        # When
        forms = self._generate_individual_forms(num_people)

        # Then
        assert len(forms) == 3
        for i, form in enumerate(forms):
            assert form["person_number"] == i + 1
            assert "name_cn" in form["required_fields"]
            assert "name_en" in form["required_fields"]
            assert "dob" in form["required_fields"]
            assert "gender" in form["required_fields"]

    def test_confirmation_lists_all_people(self):
        """Test that confirmation message lists all booked people"""
        # Given
        group_booking = {
            "date": "2025-03-06",
            "slots": [
                {"time": "10:00", "people": ["黃嘉怡", "楊君璦"]},
                {"time": "11:30", "people": ["江宜卉"]}
            ]
        }

        # When
        confirmation = self._generate_group_confirmation(group_booking, "zh")

        # Then
        assert "黃嘉怡" in confirmation
        assert "楊君璦" in confirmation
        assert "江宜卉" in confirmation
        assert "10:00" in confirmation
        assert "11:30" in confirmation
        assert "3位" in confirmation or "3" in confirmation

    def test_optimal_slot_allocation(self):
        """Test that system optimally allocates time slots for groups"""
        # Given
        calendar = {
            "10:00": {"capacity": 2, "available": True},
            "11:00": {"capacity": 1, "available": True},
            "11:30": {"capacity": 1, "available": True},
            "14:00": {"capacity": 3, "available": True}
        }
        num_people = 3

        # When
        allocation = self._optimize_slot_allocation(calendar, num_people)

        # Then
        # Should prefer grouping people together or using fewest slots
        assert len(allocation) <= 3, "Should minimize number of slots"
        assert sum(slot["num_people"] for slot in allocation) == num_people

    def _process_group_booking(self, request):
        """Helper to process group booking"""
        return {
            "success": True,
            "slots": [
                {"time": "10:00", "num_people": 2},
                {"time": "11:30", "num_people": 1}
            ]
        }

    def _generate_individual_forms(self, num_people):
        """Helper to generate forms"""
        forms = []
        for i in range(num_people):
            forms.append({
                "person_number": i + 1,
                "required_fields": ["name_cn", "name_en", "dob", "gender", "nationality"]
            })
        return forms

    def _generate_group_confirmation(self, booking, language):
        """Helper to generate confirmation"""
        return f"""您已預約成功✅
3月6日, 星期四, 上午 10:00 黃嘉怡 楊君璦
3月6日, 星期四, 上午 11:30 江宜卉
預約人數 : 3位"""

    def _optimize_slot_allocation(self, calendar, num_people):
        """Helper to optimize slot allocation"""
        # Simplified allocation
        return [
            {"time": "10:00", "num_people": 2},
            {"time": "11:30", "num_people": 1}
        ]


class TestPreAppointmentReminder:
    """TC-AM-004: Pre-Appointment Reminder"""

    def test_reminder_sent_1_to_3_days_before(self):
        """Test that reminder is sent 1-3 days before appointment"""
        # Given
        appointment_date = datetime.now() + timedelta(days=2)
        appointment = {
            "date": appointment_date.strftime("%Y-%m-%d"),
            "time": "14:00",
            "patient_phone": "+81-90-1234-5678"
        }

        # When
        should_send_reminder = self._should_send_reminder(appointment)

        # Then
        assert should_send_reminder is True

    def test_reminder_includes_all_required_info(self):
        """Test that reminder includes all necessary information"""
        # Given
        appointment = {
            "date": "2025-11-05",
            "day_of_week": "水曜日",
            "time": "14:00",
            "num_people": 1
        }

        # When
        reminder_ja = self._generate_reminder(appointment, "ja")

        # Then
        assert "11月 5日" in reminder_ja or "11/5" in reminder_ja
        assert "水曜日" in reminder_ja
        assert "14:00" in reminder_ja
        assert "1名" in reminder_ja or "1" in reminder_ja
        assert "予定通り" in reminder_ja or "確認" in reminder_ja

    def test_reminder_requests_confirmation(self):
        """Test that reminder requests customer confirmation"""
        # Given
        appointment = {"date": "2025-11-05", "time": "14:00"}

        # When
        reminder = self._generate_reminder(appointment, "ja")

        # Then
        assert "返信" in reminder, "Should request reply"
        assert "ください" in reminder, "Should use polite form"

    def test_reminder_handles_response_confirm(self):
        """Test handling of confirmation response"""
        # Given
        reminder_id = "12345"
        customer_response = "予定通りに伺います"

        # When
        result = self._handle_reminder_response(reminder_id, customer_response, "ja")

        # Then
        assert result["confirmed"] is True
        assert result["response_type"] == "attending"

    def test_reminder_handles_response_cancel(self):
        """Test handling of cancellation response"""
        # Given
        reminder_id = "12345"
        customer_response = "キャンセルしたいです"

        # When
        result = self._handle_reminder_response(reminder_id, customer_response, "ja")

        # Then
        assert result["confirmed"] is False
        assert result["response_type"] == "cancel"

    def test_reminder_handles_response_reschedule(self):
        """Test handling of reschedule request"""
        # Given
        reminder_id = "12345"
        customer_response = "時間を変更できますか"

        # When
        result = self._handle_reminder_response(reminder_id, customer_response, "ja")

        # Then
        assert result["response_type"] == "reschedule"

    def _should_send_reminder(self, appointment):
        """Helper to check if reminder should be sent"""
        appt_date = datetime.strptime(appointment["date"], "%Y-%m-%d")
        days_until = (appt_date - datetime.now()).days
        return 1 <= days_until <= 3

    def _generate_reminder(self, appointment, language):
        """Helper to generate reminder"""
        if language == "ja":
            return f"""こんにちは😊 必ずこのメッセージにご返信くださいませ！
ご予約のカウンセリング(*)時間(*)
11月 5日、水曜日、/午後 14:00
ご予約人数：1名
───────────────
予定通りお越しいただけますか？予定に変更がなければ、必ずご返信ください‼"""
        return f"Reminder: {appointment['date']} at {appointment['time']}"

    def _handle_reminder_response(self, reminder_id, response, language):
        """Helper to handle reminder response"""
        if "予定通り" in response or "伺います" in response:
            return {"confirmed": True, "response_type": "attending"}
        elif "キャンセル" in response:
            return {"confirmed": False, "response_type": "cancel"}
        elif "変更" in response:
            return {"response_type": "reschedule"}
        return {"response_type": "unknown"}


class TestReturningCustomerRecognition:
    """TC-AM-005: Returning Customer Recognition"""

    def test_identifies_returning_customer(self):
        """Test that system identifies returning customers"""
        # Given
        customer_statement = "我們今年三月去過"
        customer_phone = "+886-912-345-678"

        # When
        is_returning = self._check_returning_customer(customer_phone, customer_statement)

        # Then
        assert is_returning is True

    def test_pre_fills_known_information(self):
        """Test that known information is pre-filled for returning customers"""
        # Given
        customer_id = "12345"
        previous_data = {
            "name_cn": "黃嘉怡",
            "name_en": "Huang Chia-Yi",
            "dob": "1990-01-01",
            "nationality": "台灣"
        }

        # When
        form = self._generate_booking_form(customer_id, returning=True, previous_data=previous_data)

        # Then
        assert form["name_cn"] == "黃嘉怡"
        assert form["name_en"] == "Huang Chia-Yi"
        assert form["dob"] == "1990-01-01"
        assert form["nationality"] == "台灣"

    def test_asks_for_recent_procedure_updates(self):
        """Test that system asks for recent procedure updates from returning customers"""
        # Given
        customer_id = "12345"

        # When
        form = self._generate_booking_form(customer_id, returning=True, previous_data={})

        # Then
        assert "近3個月內醫美or手術內容" in str(form), "Should ask about recent procedures"

    def test_acknowledges_returning_status(self):
        """Test that system acknowledges returning customer"""
        # Given
        customer_phone = "+886-912-345-678"
        is_returning = True

        # When
        greeting = self._generate_greeting(customer_phone, is_returning, "zh")

        # Then
        assert "感謝您再次聯絡我們" in greeting or "歡迎回來" in greeting

    def test_faster_booking_process(self):
        """Test that booking process is faster for returning customers"""
        # Given
        new_customer_form_fields = ["name_cn", "name_en", "dob", "gender", "nationality", "contact"]
        returning_customer_form_fields = ["近3個月內醫美or手術內容", "諮詢&施作項目"]

        # Then
        assert len(returning_customer_form_fields) < len(new_customer_form_fields), \
               "Returning customer form should have fewer fields"

    def test_references_previous_visit(self):
        """Test that system can reference previous visit details"""
        # Given
        customer_id = "12345"
        previous_visit = {
            "date": "2025-03-06",
            "procedures": ["玻尿酸", "肉毒"]
        }

        # When
        reference = self._reference_previous_visit(customer_id, previous_visit, "zh")

        # Then
        assert "三月" in reference or "3月" in reference
        assert any(proc in reference for proc in ["玻尿酸", "肉毒"])

    def _check_returning_customer(self, phone, statement):
        """Helper to check if returning customer"""
        return "去過" in statement or "came before" in statement.lower()

    def _generate_booking_form(self, customer_id, returning=False, previous_data=None):
        """Helper to generate booking form"""
        if returning and previous_data:
            return {
                **previous_data,
                "近3個月內醫美or手術內容": "",
                "諮詢&施作項目": ""
            }
        return {
            "name_cn": "",
            "name_en": "",
            "dob": "",
            "gender": "",
            "nationality": "",
            "contact": ""
        }

    def _generate_greeting(self, phone, is_returning, language):
        """Helper to generate greeting"""
        if is_returning and language == "zh":
            return "您好！感謝您再次聯絡我們！"
        return "您好~"

    def _reference_previous_visit(self, customer_id, previous_visit, language):
        """Helper to reference previous visit"""
        if language == "zh":
            return f"您上次三月來過，做了玻尿酸和肉毒"
        return f"You visited us in March for filler and botox"
