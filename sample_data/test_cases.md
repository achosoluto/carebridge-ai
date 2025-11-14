# CareBridge AI Test Cases
## Based on Real Customer Chat Logs

**Version:** 1.0
**Date:** 2025-11-14
**Source Data:** 일본채팅.txt, 중국채팅.txt

---

## Table of Contents
1. [Conversation Flow Test Cases](#conversation-flow-test-cases)
2. [Multilingual Support Test Cases](#multilingual-support-test-cases)
3. [Appointment Management Test Cases](#appointment-management-test-cases)
4. [Edge Case Test Cases](#edge-case-test-cases)
5. [Integration Test Cases](#integration-test-cases)

---

## Conversation Flow Test Cases

### TC-CF-001: Initial Contact and Welcome Message
**Priority:** High
**Feature:** F01 - Multi-Channel AI Support
**Language:** Japanese, Chinese

**Test Steps:**
1. New user adds clinic as friend on messaging platform
2. System automatically sends welcome message
3. System requests required information

**Expected Result:**
- Welcome message sent within 1 second
- Message includes:
  - Greeting with user's name
  - Clinic name and services
  - List of required information (name, age, nationality, contact, consultation area, preferred date)
  - Business hours
  - Customer service hours
  - Social media links

**Test Data:**
```
Language: Japanese
User: ｱﾔﾉ
Expected greeting: "はじめまして"
```

```
Language: Chinese
User: Joy
Expected greeting: "您好!"
```

**Status:** ✅ Validated against sample data

---

### TC-CF-002: Information Collection Flow
**Priority:** High
**Feature:** F01 - Multi-Channel AI Support
**Language:** Japanese, Chinese

**Test Steps:**
1. System sends information request
2. User provides partial information
3. System validates completeness
4. System requests missing information if needed

**Required Fields:**
- Japanese consultation:
  - Name / Age / Nationality
  - Contact information
  - Consultation area (face part)
  - Preferred consultation date
  - (Optional) Arrival/departure dates for in-person

- Chinese consultation:
  - How did you hear about us
  - Consultation items
  - Appointment date & time (multiple options)
  - Number of people (excluding companions)

**Expected Result:**
- System identifies missing required fields
- Sends polite reminder for incomplete information
- Proceeds to next step only when all required info collected

**Status:** ⚠️ Needs implementation

---

### TC-CF-003: Price Inquiry Handling
**Priority:** Medium
**Feature:** F01 - Multi-Channel AI Support
**Language:** Japanese, Chinese

**Test Scenarios:**

#### Scenario A: Single Service Pricing
**Input:** "咀嚼肌肉毒、嘴唇玻尿酸 、美版超聲刀 的價錢"
**Expected Output:**
- Check if currently in business hours
- If off-hours: Send auto-reply with expected response time
- If in hours: Provide pricing information or link to current promotions
- Format prices clearly with currency (韩币)

#### Scenario B: Product Availability
**Input:** "請問有美版音波嗎"
**Expected Output:**
- Check product/equipment availability
- If unavailable: Explain status and suggest alternatives
- Response: "目前美版音波還在準備中"

**Status:** ⚠️ Needs implementation

---

### TC-CF-004: Appointment Confirmation Workflow
**Priority:** High
**Feature:** F04 - Automated Scheduling Engine
**Language:** Japanese, Chinese

**Test Steps:**
1. User requests appointment date/time
2. System checks availability
3. System collects required personal information
4. System confirms booking
5. System sends confirmation message with details

**Required Personal Information (Chinese):**
```
1. 中文名+護照上英文名
2. 西元出生年月日+性別
3. 國籍/常住國家
4. 近3個月內醫美or手術內容
5. 諮詢&施作項目
6. 是否希望當天諮詢後施作（是/否/未定）
7. 是否考慮做舒眠麻醉（是/否/未定）
```

**Expected Confirmation Message:**
```
您已預約成功✅
(*)預約時間(*)
[Date], [Day], [Time]
預約人數 : [N]位

(*)來院時，請先到9樓櫃台
並出示您的有效證件（護照或外國人登錄證）

[Additional instructions]
[Clinic address in multiple languages]
```

**Status:** ✅ Validated against sample data

---

## Multilingual Support Test Cases

### TC-ML-001: Japanese Language Processing
**Priority:** High
**Feature:** F02 - Real-Time Two-Way Translation
**Language:** Japanese

**Test Phrases:**
| Input (Japanese) | Context | Expected Understanding |
|------------------|---------|------------------------|
| "鼻のカウンセリングを検討しております" | Inquiry | Nose consultation request |
| "通訳者を連れていくことが難しいのですが大丈夫でしょうか?" | Concern | Cannot bring interpreter |
| "予定通りに伺います" | Confirmation | Will come as scheduled |
| "14:00頃に変更は可能でしょうか?" | Change request | Change time to 14:00 |

**Expected Result:**
- Accurate intent recognition for all phrases
- Appropriate contextual responses
- Polite Japanese language formality maintained

**Status:** ⚠️ Needs implementation

---

### TC-ML-002: Chinese Language Processing
**Priority:** High
**Feature:** F02 - Real-Time Two-Way Translation
**Language:** Chinese (Traditional)

**Test Phrases:**
| Input (Chinese) | Context | Expected Understanding |
|-----------------|---------|------------------------|
| "請問諮詢的話是諮詢師看完後院長會再評估一次嗎?" | Process inquiry | Consultation process with counselor and doctor |
| "中文服務都會陪同整個過程嗎?" | Service inquiry | Chinese language support throughout |
| "我們在捷運站 因為新沙悠遊卡問題卡住" | Delay notification | Delayed due to metro card issue |
| "稍等我們一下 不好意思" | Apology | Running late, please wait |

**Expected Result:**
- Accurate intent recognition
- Culturally appropriate responses
- Simplified vs Traditional Chinese handling

**Status:** ⚠️ Needs implementation

---

### TC-ML-003: Medical Terminology Translation
**Priority:** High
**Feature:** F02 - Real-Time Two-Way Translation
**Languages:** Japanese, Chinese, Korean, English

**Medical Terms Test Set:**

| Korean | Japanese | Chinese | English | Context |
|--------|----------|---------|---------|---------|
| 코 성형 | 鼻整形 | 鼻整形 | Nose surgery | Procedure |
| 보톡스 | ボトックス | 肉毒 | Botox | Treatment |
| 히알루론산 필러 | ヒアルロン酸フィラー | 玻尿酸 | Hyaluronic acid filler | Treatment |
| 사후관리 | 術後ケア | 術後護理 | Aftercare | Post-op |
| 부기 | 腫れ | 腫脹 | Swelling | Side effect |
| 실밥 제거 | 抜糸 | 拆線 | Stitch removal | Procedure |

**Expected Result:**
- Accurate medical term translation across all 4 languages
- Context-aware terminology (formal medical vs colloquial)
- Consistency in terminology throughout conversation

**Status:** ⚠️ Needs implementation

---

## Appointment Management Test Cases

### TC-AM-001: Date Availability Check
**Priority:** High
**Feature:** F04 - Automated Scheduling Engine

**Test Steps:**
1. User requests specific date
2. System checks calendar availability
3. System responds with availability status

**Scenarios:**

#### Scenario A: Date Fully Booked
**Input:** "3/7 早上10:30 3位"
**Expected:** "3/7 目前都滿囉"
**Action:** Suggest alternative dates

#### Scenario B: Date Partially Available
**Input:** "3/6呢"
**Expected:** "3/6 10點兩位 11:30一位 這樣可以"
**Action:** Offer split time slots

#### Scenario C: Date Available
**Input:** "11/13可以預約兩位嗎?"
**Expected:** Confirm availability and provide time options

**Status:** ✅ Validated against sample data

---

### TC-AM-002: Appointment Time Change
**Priority:** High
**Feature:** F04 - Automated Scheduling Engine
**Language:** Japanese

**Test Steps:**
1. Existing appointment confirmed
2. User requests time change
3. System checks new time availability
4. System updates booking
5. System sends confirmation of change

**Example Flow:**
```
Original: 11月5日17:00
Request: "14:00頃に変更は可能でしょうか?"
Response: "14:00に変更致しました！"
Confirmation: Updated time shown in reminder
```

**Expected Result:**
- Original appointment cancelled
- New time slot reserved
- Confirmation message sent
- Updated reminder sent closer to appointment

**Status:** ✅ Validated against sample data

---

### TC-AM-003: Multi-Person Booking
**Priority:** Medium
**Feature:** F04 - Automated Scheduling Engine
**Language:** Chinese

**Test Steps:**
1. User requests booking for multiple people (3 people)
2. System provides available slots for group size
3. System may split group into different time slots if needed
4. System collects individual information for each person
5. System sends individual confirmations

**Example:**
```
Request: 3 people for 3/6
Response: 10:00 (2 people), 11:30 (1 person)
Information: Collected separately for each person
Confirmation: All 3 people listed with their respective times
```

**Expected Result:**
- Optimal time slot allocation
- Individual data collection forms
- Clear breakdown of who is scheduled when
- Same-day or separated as needed

**Status:** ✅ Validated against sample data

---

### TC-AM-004: Pre-Appointment Reminder
**Priority:** High
**Feature:** F04 - Automated Scheduling Engine
**Languages:** Japanese, Chinese

**Timing:** 1-3 days before appointment

**Test Steps:**
1. System identifies upcoming appointments
2. System sends reminder message
3. System requests confirmation
4. System handles response (confirm/cancel/reschedule)

**Expected Reminder Format (Japanese):**
```
こんにちは😊 必ずこのメッセージにご返信くださいませ！
ご予約のカウンセリング(*)時間(*)
[Date], [Day], /[Time]
ご予約人数：[N]名
───────────────
予定通りお越しいただけますか？予定に変更がなければ、必ずご返信ください‼
```

**Expected Reminder Format (Chinese):**
```
您好😊 請務必回覆此條內容！
您的面診(*)預約時間(*)
[Date], [Day], [Time]
預約人數 : [N]位
───────────────
請問可以準時過來嗎？如果行程沒有變動，請務必回覆喔‼
```

**Status:** ✅ Validated against sample data

---

### TC-AM-005: Returning Customer Recognition
**Priority:** Medium
**Feature:** F01 - Multi-Channel AI Support

**Test Steps:**
1. Previous customer initiates new booking
2. System checks customer history
3. System acknowledges returning status
4. System pre-fills known information
5. System asks for updates to medical history

**Example:**
```
Customer states: "我們今年三月去過"
System response: References previous visit
System action: Pre-fills name, DOB, nationality
System asks: Recent procedures in last 3 months
```

**Expected Result:**
- Customer identified from records
- Reduced information collection (only updates needed)
- Acknowledgment: "感謝您再次聯絡我們！"
- Faster booking process

**Status:** ⚠️ Needs implementation

---

## Edge Case Test Cases

### TC-EC-001: Off-Hours Auto-Reply
**Priority:** High
**Feature:** F01 - Multi-Channel AI Support
**Languages:** Japanese, Chinese

**Business Hours:**
```
Monday-Friday: 10:00 - 19:00
Saturday: 10:00 - 16:00 (Chinese) / 17:00 (Japanese)
Sunday/Holidays: Closed
```

**Test Steps:**
1. User sends message outside business hours
2. System detects timestamp
3. System sends auto-reply
4. System queues message for staff response

**Expected Auto-Reply (Chinese):**
```
您好，目前不是我們的客服在線時間。
如果您有任何問題，歡迎先留言，我們會在上線後盡快為您回覆，非常感謝您的耐心等候！
(*)此訊息為自動回覆，回覆將依照訊息傳送的先後順序進行處理，重複傳送可能會延長等候時間，敬請耐心等候。
```

**Status:** ✅ Validated against sample data

---

### TC-EC-002: Last-Minute Delay Notification
**Priority:** Medium
**Feature:** F01 - Multi-Channel AI Support
**Language:** Chinese

**Test Steps:**
1. Customer on way to appointment encounters delay
2. Customer sends notification message
3. System acknowledges and reassures
4. System notifies clinic staff

**Example Messages:**
```
Customer: "不好意思我們在捷運站 因為新沙悠遊卡問題卡住 稍等我們一下 不好意思🙏🙏"
System: "好的"
Customer: "我們出來了！上樓中 謝謝你🙏"
System: "沒事不客氣~等下見"
```

**Expected Result:**
- Polite acknowledgment
- Reassurance (not overly concerned)
- Brief responses appropriate to situation
- Staff notified of delay

**Status:** ✅ Validated against sample data

---

### TC-EC-003: Incomplete Information Submission
**Priority:** High
**Feature:** F01 - Multi-Channel AI Support

**Test Steps:**
1. User submits booking request
2. User provides incomplete information
3. System identifies missing required fields
4. System sends specific request for missing data

**Example:**
```
Missing: Passport English name
System: Reminds user to provide passport name
System: Explains importance (Korean hospital real-name system)
```

**Expected Result:**
- Specific identification of missing fields
- Polite request for completion
- Explanation of why information is needed
- Booking not confirmed until complete

**Status:** ⚠️ Needs implementation

---

### TC-EC-004: Language Barrier and Interpreter Needs
**Priority:** Medium
**Feature:** F02 - Real-Time Two-Way Translation
**Language:** Japanese

**Test Steps:**
1. Customer asks about interpreter requirements
2. System assesses consultation type (online vs in-person)
3. System provides appropriate guidance

**Example Flow:**
```
Customer: "通訳者を連れていくことが難しいのですが大丈夫でしょうか?"
System: "大丈夫ですよ"
Note: Online consultation available in Japanese
Note: In-person consultation may need interpreter
```

**Expected Result:**
- Clear explanation of language support options
- Online vs in-person differences explained
- Accommodation offered when possible
- Staff arranged for language support if needed

**Status:** ✅ Validated against sample data

---

### TC-EC-005: Product/Service Unavailability
**Priority:** Low
**Feature:** F01 - Multi-Channel AI Support
**Language:** Chinese

**Test Steps:**
1. Customer inquires about specific product/service
2. System checks availability
3. If unavailable: System explains status
4. System suggests alternatives if available

**Example:**
```
Customer: "請問有美版音波嗎"
System: "目前美版音波還在準備中"
Action: Suggest alternative treatments
```

**Expected Result:**
- Honest answer about availability
- Status explanation (coming soon, discontinued, etc.)
- Alternative suggestions
- Offer to notify when available

**Status:** ✅ Validated against sample data

---

### TC-EC-006: Duplicate/Repeated Messages
**Priority:** Low
**Feature:** F01 - Multi-Channel AI Support

**Test Steps:**
1. User sends same inquiry multiple times
2. System detects duplicate messages
3. System sends reminder about queue

**Expected Response:**
```
"回覆將依照訊息傳送的先後順序進行，重複發送可能會延長等候時間，敬請耐心等待"
```

**Expected Result:**
- Polite reminder sent once
- Queue position not affected negatively
- Response sent to latest message
- Previous duplicates ignored

**Status:** ⚠️ Needs implementation

---

## Integration Test Cases

### TC-IN-001: End-to-End Appointment Flow (Japanese)
**Priority:** Critical
**Features:** F01, F02, F04
**Language:** Japanese

**Complete User Journey:**

1. **Initial Contact**
   - User adds clinic as friend
   - Welcome message received (TC-CF-001)

2. **Information Gathering**
   - User asks about nose consultation
   - System requests additional details (TC-CF-002)

3. **Appointment Scheduling**
   - User provides preferred date/time
   - System checks availability (TC-AM-001)
   - System suggests available slot

4. **Detail Collection**
   - System requests full name (passport)
   - User provides information
   - Booking confirmed (TC-CF-004)

5. **Pre-Appointment**
   - Reminder sent 1-3 days before (TC-AM-004)
   - User confirms attendance

6. **Appointment Modification**
   - User requests time change (TC-AM-002)
   - System accommodates
   - New confirmation sent

7. **Day of Appointment**
   - Final confirmation received
   - User arrives and checks in

8. **Post-Consultation**
   - System sends procedure summary
   - System sends aftercare instructions
   - Follow-up scheduled

**Expected Success Criteria:**
- All messages in proper Japanese
- No information lost between steps
- Smooth handoff between automated and human staff
- Customer satisfaction maintained throughout

**Status:** ⚠️ Needs full integration testing

---

### TC-IN-002: End-to-End Multi-Person Booking (Chinese)
**Priority:** Critical
**Features:** F01, F02, F04
**Language:** Chinese (Traditional)

**Complete User Journey:**

1. **Initial Contact**
   - Welcome message with promotions

2. **Service Inquiry**
   - Multiple pricing questions (TC-CF-003)
   - Product availability checks (TC-EC-005)

3. **Consultation Process Questions**
   - Service flow clarification
   - Language support confirmation (TC-EC-004)

4. **Group Booking**
   - Request for 3 people (TC-AM-003)
   - Date unavailable, alternative offered (TC-AM-001)
   - Split time slots arranged

5. **Individual Data Collection**
   - Separate forms for each person (TC-CF-004)
   - Medical history collected
   - All bookings confirmed

6. **Additional Inquiries**
   - Ongoing pricing questions
   - Product detail questions

7. **Pre-Appointment Reminder**
   - Confirmation requested (TC-AM-004)
   - User confirms

8. **Day-of Delay**
   - Last-minute delay notification (TC-EC-002)
   - System handles gracefully

9. **Post-Treatment**
   - Individual aftercare instructions sent to each person
   - Different procedures, different instructions

10. **Future Booking**
    - Returning customer months later (TC-AM-005)
    - Faster process with history

**Expected Success Criteria:**
- All 3 people tracked individually
- Correct instructions sent to each person
- Returning customer recognized
- Traditional Chinese maintained throughout

**Status:** ⚠️ Needs full integration testing

---

### TC-IN-003: Multilingual Translation Accuracy
**Priority:** High
**Features:** F01, F02
**Languages:** Korean ↔ Japanese ↔ Chinese ↔ English

**Test Steps:**
1. Customer sends message in Japanese
2. System translates to Korean for staff
3. Staff responds in Korean
4. System translates back to Japanese
5. Verify accuracy and meaning preservation

**Critical Translation Points:**
- Medical terminology (TC-ML-003)
- Polite/formal language levels
- Cultural context (honorifics, formality)
- Time/date formats
- Currency and pricing

**Expected Result:**
- <5% translation error rate
- No medical terminology mistakes
- Cultural appropriateness maintained
- Staff and customer both understand clearly

**Status:** ⚠️ Needs implementation

---

### TC-IN-004: Business Hours and Auto-Response
**Priority:** High
**Features:** F01
**Languages:** All

**Test Scenarios:**

| Day | Time | Input Language | Expected Response |
|-----|------|----------------|-------------------|
| Monday | 09:00 | Chinese | Auto-reply (off-hours) |
| Monday | 10:00 | Chinese | Human/AI response (in hours) |
| Friday | 19:00 | Japanese | Auto-reply (after hours) |
| Saturday | 15:00 | Chinese | Human/AI response (in hours) |
| Saturday | 17:00 | Japanese | Auto-reply (after hours) |
| Sunday | 12:00 | Any | Auto-reply (closed) |

**Expected Result:**
- Correct auto-reply detection based on day/time
- Messages queued for next business day
- Staff alerted to waiting messages
- Response sent in same language as inquiry

**Status:** ⚠️ Needs implementation

---

## Test Data Summary

### Customer Personas from Sample Data

#### Persona 1: NAK********* (Japanese)
- **Language:** Japanese
- **Service:** Nose consultation
- **Characteristics:**
  - First-time patient
  - Previous filler experience
  - Found via Twitter
  - Cannot bring interpreter
  - Requests time change
- **Journey:** Inquiry → Booking → Change → Confirmation → Attendance → Post-consultation

#### Persona 2: Huang **** (Chinese)
- **Language:** Traditional Chinese
- **Service:** Multiple services (botox, fillers, ultrasound, RF)
- **Characteristics:**
  - Books for groups (3 people)
  - Very detail-oriented, asks many questions
  - Returning customer (came in March, books again in November)
  - Found via Instagram
  - Experiences last-minute delay
- **Journey:** Multiple interactions over 8+ months, group bookings, repeat customer

### Real Conversation Metrics

**Japanese Chat (139 lines):**
- Messages from clinic: ~12
- Messages from customer: ~11
- Average response time: Same day
- Appointment changes: 1
- Language barrier discussion: Yes
- Successful outcome: Yes (attended consultation)

**Chinese Chat (567 lines):**
- Messages from clinic: ~25
- Messages from customer: ~22
- Average response time: Same day (with off-hours delays)
- Bookings made: 2 (March and November)
- People booked: 5 total (3 in March, 2 in November)
- Language support questions: Yes
- Last-minute delays: 1
- Successful outcomes: Yes (all attended)

---

## Test Automation Recommendations

### Priority 1 (Immediate)
1. TC-CF-001: Welcome message automation
2. TC-AM-001: Date availability checking
3. TC-EC-001: Off-hours auto-reply
4. TC-ML-003: Medical terminology translation

### Priority 2 (Short-term)
1. TC-CF-004: Appointment confirmation workflow
2. TC-AM-004: Pre-appointment reminders
3. TC-IN-004: Business hours handling
4. TC-AM-002: Appointment modifications

### Priority 3 (Medium-term)
1. TC-AM-003: Multi-person booking logic
2. TC-AM-005: Returning customer recognition
3. TC-CF-003: Price inquiry handling
4. TC-IN-003: Translation accuracy testing

### Priority 4 (Long-term)
1. TC-IN-001: End-to-end Japanese flow
2. TC-IN-002: End-to-end Chinese flow
3. Full conversation AI training
4. Sentiment analysis and satisfaction tracking

---

## Success Metrics

### Automated Response Accuracy
- **Target:** 85%+ correct automated responses
- **Measurement:** % of messages handled without human intervention

### Response Time
- **Target:** <2 seconds for automated responses
- **Measurement:** Time from message receipt to response sent

### Translation Accuracy
- **Target:** 95%+ accurate translations
- **Measurement:** Human evaluation of random sample

### Appointment Booking Success Rate
- **Target:** 90%+ completion rate
- **Measurement:** (Completed bookings / Initiated bookings) * 100

### Customer Satisfaction
- **Target:** 4.2/5.0 CSAT score
- **Measurement:** Post-interaction surveys

### Language Detection Accuracy
- **Target:** 99%+ correct language identification
- **Measurement:** Automated language detection validation

---

## Notes

- All test cases derived from real customer conversations
- Maintains HIPAA compliance requirements
- Personal information redacted with ****
- Edge cases represent actual customer behaviors
- Translation requirements based on real multilingual needs

**Document Status:** ✅ Complete
**Next Review:** After initial implementation phase
**Maintained by:** CareBridge AI Development Team
