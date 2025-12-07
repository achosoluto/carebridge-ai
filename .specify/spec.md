# CareBridge AI - Simplified Specification

## Overview
A simple web application that helps Korean plastic surgery clinics communicate with Japanese and Chinese patients through real-time translation and basic appointment booking.

**Important Note**: Japanese customers primarily use Line, while Chinese customers use WeChat for messaging. The system focuses on web-based communication to avoid complex integrations, but clinic staff should be aware of these dominant platforms when directing patients to the web interface.

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

## Key Features (Simplified)
- **Translation Service**: Korean ↔ Japanese/Chinese for medical terms
- **Patient Messaging**: Simple chat interface
- **Appointment Booking**: Basic calendar and form
- **Staff Dashboard**: Clean interface for daily operations

## What We Don't Need
- Complex AI chatbots (staff prefer human interaction)
- Advanced scheduling algorithms (clinic has simple availability)
- Multi-channel integrations (web messaging is sufficient)
- Enterprise analytics (basic usage reports enough)

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