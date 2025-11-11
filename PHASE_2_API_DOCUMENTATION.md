# CareBridge AI - Phase 2 API Documentation

## Overview

Phase 2 introduces advanced features for the CareBridge AI healthcare platform:
- **Real-time Translation** with Google Translate API integration
- **Advanced Scheduling Optimization** with AI-powered recommendations
- **Medical Terminology Management** for accurate healthcare translations
- **Appointment Waitlist System** for fully booked slots
- **Multi-channel Notifications** for appointment reminders

**Base URL:** `http://localhost:8000/api/`

---

## Authentication

Currently, all endpoints are open for development. In production, implement token-based authentication.

---

## Translation API

### 1. Translate Text

Translate text using Google Translate API with medical terminology enhancement.

**Endpoint:** `POST /api/translations/translate/`

**Request Body:**
```json
{
  "text": "안녕하세요, 코 성형 상담 예약하고 싶습니다",
  "target_language": "en",
  "source_language": "auto",
  "message_id": 123
}
```

**Response:**
```json
{
  "translated_text": "Hello, I would like to schedule a rhinoplasty consultation",
  "source_language": "ko",
  "target_language": "en",
  "processing_time_ms": 245,
  "skipped": false
}
```

**Supported Languages:** `ko`, `en`, `zh`, `ja`

---

### 2. Get Translation Statistics

Get translation performance metrics.

**Endpoint:** `GET /api/translations/stats/?days=30`

**Response:**
```json
{
  "total_translations": 1250,
  "medical_translations": 450,
  "average_processing_time_ms": 187.5,
  "average_quality_score": 0.94,
  "period_days": 30
}
```

---

### 3. Rate Translation Quality

Provide feedback on translation quality.

**Endpoint:** `POST /api/translations/{id}/rate_quality/`

**Request Body:**
```json
{
  "quality_score": 0.95
}
```

**Response:**
```json
{
  "success": true,
  "translation_id": 123,
  "quality_score": 0.95
}
```

---

### 4. Get Translation History

List all translation history with pagination.

**Endpoint:** `GET /api/translations/`

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)

**Response:**
```json
{
  "count": 1250,
  "next": "http://localhost:8000/api/translations/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "source_text": "안녕하세요",
      "translated_text": "Hello",
      "source_language": "ko",
      "target_language": "en",
      "translation_service": "google",
      "confidence_score": 0.98,
      "quality_score": 0.95,
      "is_medical_terminology": false,
      "processing_time_ms": 150,
      "created_at": "2025-11-11T10:30:00Z"
    }
  ]
}
```

---

## Medical Terminology API

### 1. List Medical Terms

Get all medical terminology with translations.

**Endpoint:** `GET /api/medical-terms/`

**Query Parameters:**
- `category`: Filter by category (e.g., `procedure`, `treatment`)

**Response:**
```json
{
  "count": 15,
  "results": [
    {
      "id": 1,
      "term_en": "rhinoplasty",
      "term_ko": "코 성형",
      "term_zh": "鼻整形",
      "term_ja": "鼻形成",
      "category": "procedure",
      "description": "Nose reshaping surgery",
      "usage_count": 45,
      "accuracy_rating": 0.98,
      "created_at": "2025-11-11T10:00:00Z"
    }
  ]
}
```

---

### 2. Search Medical Terms

Search medical terminology by keyword.

**Endpoint:** `GET /api/medical-terms/search/?q=surgery&lang=en`

**Response:**
```json
{
  "results": [
    {
      "id": 2,
      "term_en": "surgery",
      "term_ko": "수술",
      "term_zh": "手术",
      "term_ja": "手術",
      "category": "procedure"
    }
  ]
}
```

---

### 3. Get Term Categories

List all medical term categories.

**Endpoint:** `GET /api/medical-terms/categories/`

**Response:**
```json
{
  "categories": [
    "general",
    "procedure",
    "treatment",
    "medication",
    "condition",
    "symptom"
  ]
}
```

---

## Doctor Management API

### 1. List Doctors

Get all doctors with their information.

**Endpoint:** `GET /api/doctors/`

**Query Parameters:**
- `is_active`: Filter by active status (`true`/`false`)

**Response:**
```json
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "name": "Dr. Kim Min-jun",
      "specialization": "Plastic Surgery",
      "email": "kim.minjun@carebridge.ai",
      "phone": "+82-10-1234-5678",
      "is_active": true,
      "max_daily_appointments": 20,
      "average_appointment_duration": "00:30:00",
      "created_at": "2025-11-11T10:00:00Z"
    }
  ]
}
```

---

### 2. Get Doctor Availability

Get doctor's weekly availability schedule.

**Endpoint:** `GET /api/doctors/{id}/availability/`

**Response:**
```json
[
  {
    "id": 1,
    "doctor": 1,
    "doctor_name": "Dr. Kim Min-jun",
    "weekday": 0,
    "weekday_display": "Monday",
    "start_time": "09:00:00",
    "end_time": "18:00:00",
    "is_available": true
  }
]
```

---

### 3. Get Doctor Workload

Get doctor's current appointment workload.

**Endpoint:** `GET /api/doctors/{id}/workload/`

**Response:**
```json
{
  "doctor_id": 1,
  "doctor_name": "Dr. Kim Min-jun",
  "max_daily_appointments": 20,
  "upcoming_appointments": 45,
  "daily_breakdown": {
    "2025-11-12": 8,
    "2025-11-13": 12,
    "2025-11-14": 10,
    "2025-11-15": 15
  }
}
```

---

## Scheduling Optimization API

### 1. Find Available Slots

Find available appointment slots for a doctor.

**Endpoint:** `POST /api/scheduling/available-slots/`

**Request Body:**
```json
{
  "doctor_id": 1,
  "start_date": "2025-11-15",
  "end_date": "2025-11-22",
  "preferred_time": "morning"
}
```

**Preferred Time Options:** `morning`, `afternoon`, `evening`, `any`

**Response:**
```json
{
  "doctor_id": 1,
  "doctor_name": "Dr. Kim Min-jun",
  "available_slots": [
    "2025-11-15T09:00:00Z",
    "2025-11-15T09:30:00Z",
    "2025-11-15T10:00:00Z",
    "2025-11-15T10:30:00Z"
  ],
  "total_slots": 48
}
```

---

### 2. Optimize Appointment Schedule

Get AI-powered appointment recommendations with wait time reduction.

**Endpoint:** `POST /api/scheduling/optimize/`

**Request Body:**
```json
{
  "patient_id": 1,
  "doctor_id": 1,
  "procedure_type_id": 1,
  "requested_time": "2025-11-15T14:00:00Z",
  "preferences": {
    "preferred_time": "morning"
  }
}
```

**Response:**
```json
{
  "success": true,
  "optimization": {
    "patient_id": 1,
    "doctor": "Dr. Kim Min-jun",
    "procedure": "1",
    "original_time": "2025-11-15T14:00:00Z",
    "optimized_time": "2025-11-15T10:00:00Z",
    "time_difference_minutes": 240,
    "wait_time_reduction_minutes": 30,
    "optimization_score": 0.85
  }
}
```

**Optimization Score:** 0-1 scale indicating quality of optimization
- **0.8-1.0:** Excellent optimization
- **0.6-0.8:** Good optimization
- **0.4-0.6:** Moderate optimization
- **<0.4:** Minimal optimization

---

## Procedure Types API

### 1. List Procedure Types

Get all available procedure types.

**Endpoint:** `GET /api/procedure-types/`

**Response:**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "name": "Rhinoplasty",
      "name_ko": "코 성형",
      "name_zh": "鼻整形",
      "name_ja": "鼻形成",
      "description": "Nose reshaping surgery",
      "estimated_duration": "02:00:00",
      "requires_equipment": "",
      "preparation_time": "00:30:00",
      "recovery_time": "01:00:00"
    }
  ]
}
```

---

### 2. Search Procedures

Search procedure types by name.

**Endpoint:** `GET /api/procedure-types/search/?q=botox&lang=en`

**Response:**
```json
{
  "results": [
    {
      "id": 3,
      "name": "Botox Treatment",
      "name_ko": "보톡스 시술",
      "estimated_duration": "00:20:00"
    }
  ]
}
```

---

## Waitlist Management API

### 1. Add to Waitlist

Add patient to appointment waitlist.

**Endpoint:** `POST /api/waitlist/add/`

**Request Body:**
```json
{
  "patient_id": 1,
  "doctor_id": 1,
  "procedure_type_id": 1,
  "preferred_date": "2025-11-20",
  "preferred_time_start": "09:00:00",
  "preferred_time_end": "12:00:00"
}
```

**Response:**
```json
{
  "success": true,
  "waitlist_id": 1,
  "position": 3,
  "priority_score": 65
}
```

---

### 2. List Waitlist Entries

Get all waitlist entries.

**Endpoint:** `GET /api/waitlist/?status=waiting`

**Status Options:** `waiting`, `notified`, `booked`, `expired`, `cancelled`

**Response:**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "patient": 1,
      "patient_name": "John Doe",
      "doctor": 1,
      "doctor_name": "Dr. Kim Min-jun",
      "procedure_type": 1,
      "procedure_name": "Rhinoplasty",
      "preferred_date": "2025-11-20",
      "preferred_time_start": "09:00:00",
      "preferred_time_end": "12:00:00",
      "status": "waiting",
      "priority_score": 65,
      "created_at": "2025-11-11T10:00:00Z"
    }
  ]
}
```

---

### 3. Process Waitlist Notifications

Process waitlist and notify patients about available slots.

**Endpoint:** `POST /api/waitlist/process_notifications/`

**Response:**
```json
{
  "success": true,
  "notifications_sent": 3
}
```

---

## Appointment Reminders API

### 1. Schedule Reminder

Schedule an appointment reminder.

**Endpoint:** `POST /api/reminders/schedule/`

**Request Body:**
```json
{
  "appointment_id": 1,
  "hours_before": 24
}
```

**Response:**
```json
{
  "success": true,
  "appointment_id": 1,
  "hours_before": 24
}
```

---

### 2. Process Pending Reminders

Send all pending reminders that are due.

**Endpoint:** `POST /api/reminders/process_pending/`

**Response:**
```json
{
  "success": true,
  "reminders_sent": 5
}
```

---

### 3. List Reminders

Get all appointment reminders.

**Endpoint:** `GET /api/reminders/`

**Response:**
```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "appointment": 1,
      "scheduled_send_at": "2025-11-14T10:00:00Z",
      "sent_at": "2025-11-14T10:00:15Z",
      "channel": "sms",
      "status": "sent",
      "message_content": "Appointment reminder: Dr. Kim Min-jun...",
      "error_message": "",
      "created_at": "2025-11-13T10:00:00Z"
    }
  ]
}
```

**Reminder Status:** `pending`, `sent`, `failed`, `cancelled`

**Channels:** `sms`, `email`, `kakao`, `wechat`, `line`

---

## Error Responses

All endpoints return standard error responses:

### 400 Bad Request
```json
{
  "error": "Invalid request parameters",
  "details": {
    "field_name": ["Error message"]
  }
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "message": "Detailed error message"
}
```

---

## Rate Limiting

**Current Status:** Not implemented (development mode)

**Production Recommendations:**
- 100 requests per minute per IP for general endpoints
- 20 requests per minute for translation endpoints
- 10 requests per minute for optimization endpoints

---

## Performance Metrics

### Translation API
- **Target Response Time:** <1 second
- **Medical Terminology Accuracy:** 95%+
- **Cache Hit Rate:** 60%+

### Scheduling Optimization
- **Target Wait Time Reduction:** 30%
- **Optimization Success Rate:** 85%+
- **Slot Finding Time:** <500ms

---

## Testing Endpoints

Use the following curl commands to test the API:

### Test Translation
```bash
curl -X POST http://localhost:8000/api/translations/translate/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "안녕하세요",
    "target_language": "en",
    "source_language": "auto"
  }'
```

### Test Available Slots
```bash
curl -X POST http://localhost:8000/api/scheduling/available-slots/ \
  -H "Content-Type: application/json" \
  -d '{
    "doctor_id": 1,
    "start_date": "2025-11-15",
    "end_date": "2025-11-22",
    "preferred_time": "morning"
  }'
```

### Test Waitlist Addition
```bash
curl -X POST http://localhost:8000/api/waitlist/add/ \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 1,
    "doctor_id": 1,
    "procedure_type_id": 1,
    "preferred_date": "2025-11-20",
    "preferred_time_start": "09:00:00",
    "preferred_time_end": "12:00:00"
  }'
```

---

## Next Steps

1. **Frontend Integration:** Update React frontend to use new Phase 2 endpoints
2. **Authentication:** Implement JWT token authentication
3. **Rate Limiting:** Add Django REST Framework throttling
4. **Monitoring:** Set up API usage monitoring and analytics
5. **Documentation:** Generate OpenAPI/Swagger documentation
6. **Testing:** Create comprehensive API test suite

---

## Support

For questions or issues, contact the development team or refer to the main README.md file.