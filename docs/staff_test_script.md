# CareBridge AI Staff Test Script

## Objective
This script outlines the process steps that Korean medical staff will take when using the CareBridge AI system to communicate with Japanese and Chinese patients, schedule appointments, and manage patient information.

## Scenario 1: New Patient Inquiry (Based on Japanese sample chat)

### Step 1: Patient Registration
1. Navigate to the Patients page in CareBridge AI
2. Click on "Add Patient" button
3. Enter patient information:
   - Name: "NAK*********" 
   - Language: "JA" (Japanese)
   - Contact Info: (as provided by patient)
4. Submit patient record

### Step 2: Initial Consultation Request
1. Go to the Messages section
2. Select the newly added patient
3. Receive auto-translated message from patient:
   - Original: "鼻のカウンセリングを検討しております。 11月5日16:00以降で空いている時間はありますでしょうか?"
   - Translated: [Korean translation about nose consultation inquiry for Nov 5 after 4pm]
4. Respond in Korean in the messaging interface
5. Message will be auto-translated to Japanese for patient

### Step 3: Appointment Booking
1. Access the Appointments section
2. Check availability for November 5th
3. Find available slot at 17:00 (5:00 PM)
4. Create appointment:
   - Patient: NAK*********
   - Doctor: Dr. Jung Nam-ju (as requested by patient)
   - Date: November 5, 2025
   - Time: 17:00
   - Status: PENDING

### Step 4: Time Change Request
1. Receive patient request for time change: "14:00頃に変更は可能でしょうか?"
2. Update appointment time from 17:00 to 14:00 (2:00 PM)
3. System automatically notifies patient of change
4. Verify in appointment calendar that time has been updated

### Step 5: Pre-Visit Confirmation
1. Send confirmation message to patient using patient list feature:
   - Date: November 5, Wednesday
   - Time: 14:00
   - Number of people: 1
2. Patient confirms: "明日予定通りに伺います"
3. Update appointment status to CONFIRMED

### Step 6: Post-Consultation Documentation
1. After consultation, update patient record with:
   - Treatment recommendations
   - Surgical details (non-prosthesis method)
   - Follow-up schedule
   - Post-operative care instructions

## Scenario 2: Group Appointment (Based on Chinese sample chat)

### Step 1: Multiple Patient Registration
1. Navigate to Patients page
2. Register three patients:
   - Patient 1: Huang Jia-yi (黃嘉怡), Language: ZH (Chinese)
   - Patient 2: Yang Jun'ai (楊君璦), Language: ZH (Chinese)  
   - Patient 3: Jiang Yihui (江宜卉), Language: ZH (Chinese)
3. Enter required information for each patient

### Step 2: Group Appointment Coordination
1. Go to Appointments section
2. Check availability for March 6th
3. Find slots for multiple patients:
   - 10:00: Huang Jia-yi and Yang Jun'ai (together)
   - 11:30: Jiang Yihui
4. Create multiple appointments with appropriate details

### Step 3: Price Inquiry Management
1. When patient inquires about pricing:
   - Navigate to Messages section
   - Access patient conversation
   - Provide translated pricing information:
     - Botox: 990,000 KRW for jaw muscle
     - Hyaluronic acid: 1,650,000 KRW per cc
2. System auto-translates Korean pricing to Chinese for patient

### Step 4: Post-Treatment Instructions
1. After treatment completion
2. Use system to send post-treatment care instructions
3. System auto-translates instructions to patient's preferred language
4. Document treatment details in patient records

## Scenario 3: Regular Workflow

### Daily Patient Communication
1. Log into CareBridge AI staff portal
2. Check Messages section for new translations
3. Review auto-translated messages from Japanese/Chinese patients
4. Respond in Korean (system translates back to patient language)
5. Monitor conversation history for follow-up requirements

### Appointment Management
1. View daily/weekly appointment calendar
2. Filter by doctor, patient language, or appointment status
3. Update appointment statuses (PENDING → CONFIRMED → COMPLETED)
4. Handle cancellations and rescheduling requests
5. Send automated confirmations to patients

### Patient Record Management
1. Access patient database sorted by language preference
2. Update patient contact information and medical history
3. Track previous treatments and consultations
4. Generate reports for administrative purposes

## System Verification Points

### Authentication
- Staff members must log in with valid credentials
- JWT token authentication protects all patient data
- Session management ensures security

### Translation Functionality  
- Messages automatically translate between Korean and patient languages
- Original and translated texts are both stored
- Translation accuracy is maintained for medical terminology

### Data Persistence
- Patient records persist in PostgreSQL database
- Appointment information is maintained with status changes
- Message history is preserved for future reference

### User Interface
- Intuitive dashboard for staff operations
- Clear language indicators for patient management
- Responsive design for tablet/desktop use