# CareBridge AI - Simplified Specification

## Overview
A simple web application that helps Korean plastic surgery clinics communicate with Japanese and Chinese patients through real-time translation and basic appointment booking.

**Important Note**: Japanese customers primarily use Line, while Chinese customers use WeChat for messaging. The system focuses on web-based communication to avoid complex integrations, but clinic staff should be aware of these dominant platforms when directing patients to the web interface.
**Interface Language**: The entire staff interface must be in **Korean** to accommodate the primary users (Korean clinic staff).

## Who Uses It
- **Korean Clinic Staff**: Doctors and receptionists who speak Korean
- **Japanese/Chinese Patients**: International patients seeking plastic surgery procedures

## What Success Looks Like
- Korean staff can read and respond to patient messages in Japanese/Chinese
- Patients can send inquiries in their native language
- Staff can book appointments without language barriers
- Simple, reliable system that works during busy clinic hours

## User Journeys

### Patient Journey
1. Patient visits clinic website
2. Sends message in Japanese/Chinese about procedure interest
3. Receives translated response from Korean staff
4. Books appointment through simple form
5. Gets confirmation in their language

### Staff Journey  
1. Staff logs into simple dashboard
2. Sees translated patient messages
3. Responds in Korean (auto-translated to patient's language)
4. Books appointments in familiar interface
5. Manages patient communication efficiently

## Key Features (Enhanced)
- **Seamless Booking Experience**: Self-service booking with real-time availability and automated confirmations. Eliminates manual back-and-forth.
- **Instant Access to Information**: 24/7 chatbot for procedure costs, care instructions, and recommendations.
- **Staff Efficiency Optimization**: Automated reminders, pre-filled patient data, and usage analytics.
- **Translation Service**: Korean ↔ Japanese/Chinese for medical terms
- **Staff Dashboard**: Clean interface for daily operations

## Detailed Feature Specifications

### 1. Seamless Booking Experience
- **User Story**: As a patient, I want to view available slots and book my own appointment without waiting for a staff reply.
- **Acceptance Criteria**:
    - Patient-facing booking portal (web).
    - Real-time sync with doctor availability.
    - Automated confirmation email/message in patient's language.

### 2. Instant Access to Information
- **User Story**: As a patient, I want immediate answers to common questions about pricing and recovery at any time of day.
- **Acceptance Criteria**:
    - AI-powered Chatbot accessible on the website.
    - Knowledge base of FAQs (Pricing, Procedures, Post-op care).
    - Handoff to human staff for complex queries.

### 3. Staff Efficiency Optimization
- **User Story**: As a staff member, I want the system to handle routine reminders so I can focus on patient care.
- **Acceptance Criteria**:
    - Automated appointment reminders (Email/SMS).
    - Pre-filled patient forms (intake).
    - Analytics dashboard showing patient volume and popular procedures.

## What We Don't Need
- Multi-channel integrations (Line/WeChat API deep integration is still avoided, keep web-based).

## Success Metrics
- Staff can handle international patients without language stress
- Patients feel understood and well-cared for
- Clinic can expand international patient base
- System works reliably without constant maintenance

## Constraints
- Must work on clinic computers (no fancy requirements)
- Simple deployment (no complex DevOps)
- Korean staff training should take < 1 hour
- System should handle clinic's patient load easily