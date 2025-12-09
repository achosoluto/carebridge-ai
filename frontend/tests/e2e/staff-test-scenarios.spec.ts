import { test, expect } from '@playwright/test';

test.describe('Staff Test Scenarios', () => {
  test.beforeEach(async ({ page }) => {
    // Set up test authentication
    await page.addInitScript(() => {
      localStorage.setItem('token', 'testtoken123');
    });
  });

  // Test scenario 1: New Patient Inquiry (Japanese)
  test('Scenario 1: New Patient Inquiry (Japanese)', async ({ page }) => {
    // Navigate to dashboard (already authenticated via beforeEach)
    await page.goto('/');

    // Wait for dashboard to load
    await expect(page.locator('h2')).toContainText('Dashboard');

    // Step 1: Patient Registration - Navigate to patients page
    await page.goto('/patients');
    await expect(page.locator('h2')).toContainText('Patients');

    // Click Add Patient button (assuming there's a button with this text or similar)
    await page.click('button:has-text("Add")');

    // Fill patient information
    await page.fill('input[name="name"]', 'NAK*********');
    await page.selectOption('select[name="language"]', 'JA');
    await page.fill('input[name="contact_info"]', 'nak@example.com');
    await page.click('button:has-text("Save")');

    // Wait for success message or patient to appear in list
    await expect(page.locator('text=NAK*********')).toBeVisible();

    // Step 2: Initial Consultation Request - Navigate to messages
    await page.goto('/messages');
    await expect(page.locator('h2')).toContainText('Messages');

    // Select the newly added patient
    await page.click('text=NAK*********');

    // Verify auto-translated message from patient
    await expect(page.locator('.message')).toContainText('코 상담을 고려하고 있습니다');

    // Respond in Korean
    await page.fill('textarea[name="message"]', '11월 5일 17:00에 예약 가능합니다.');
    await page.click('button:has-text("Send")');

    // Verify message sent and translated
    await expect(page.locator('.message')).toContainText('11月5日17:00で予約可能です。');

    // Step 3: Appointment Booking - Navigate to appointments
    await page.goto('/appointments');
    await expect(page.locator('h2')).toContainText('Appointments');

    // Check availability for November 5th and book appointment
    await page.click('text=November 5, 2025');
    await page.click('text=17:00');

    // Verify appointment details
    await expect(page.locator('text=NAK*********')).toBeVisible();
    await expect(page.locator('text=Dr. Jung Nam-ju')).toBeVisible();
    await expect(page.locator('text=17:00')).toBeVisible();
    await expect(page.locator('text=PENDING')).toBeVisible();

    // Step 4: Time Change Request
    // Simulate patient request for time change
    await page.click('text=Edit');
    await page.selectOption('select[name="time"]', '14:00');
    await page.click('button:has-text("Update")');

    // Verify appointment time updated
    await expect(page.locator('text=14:00')).toBeVisible();

    // Step 5: Pre-Visit Confirmation
    await page.click('text=NAK*********');

    // Send confirmation message
    await page.fill('textarea[name="message"]', '明日予定通りに伺います');
    await page.click('button:has-text("Send")');

    // Update appointment status to CONFIRMED
    await page.click('text=Edit');
    await page.selectOption('select[name="status"]', 'CONFIRMED');
    await page.click('button:has-text("Update")');

    // Verify status updated
    await expect(page.locator('text=CONFIRMED')).toBeVisible();

    // Step 6: Post-Consultation Documentation
    // Update patient record with treatment details
    await page.goto('/patients');
    await page.click('text=NAK*********');

    // Update with treatment recommendations
    await page.fill('textarea[name="notes"]', 'Treatment recommendations, surgical details, follow-up schedule, post-operative care instructions');
    await page.click('button:has-text("Save")');

    await expect(page.locator('text=Success')).toBeVisible();
  });

  // Test scenario 2: Group Appointment (Chinese)
  test('Scenario 2: Group Appointment (Chinese)', async ({ page }) => {
    // Navigate to dashboard (already authenticated)
    await page.goto('/');

    // Step 1: Multiple Patient Registration
    await page.goto('/patients');

    // Register first patient
    await page.click('button:has-text("Add Patient")');
    await page.fill('input[name="name"]', 'Huang Jia-yi');
    await page.selectOption('select[name="language"]', 'ZH');
    await page.fill('input[name="contact_info"]', 'huang@example.com');
    await page.click('button:has-text("Save")');

    // Register second patient
    await page.click('button:has-text("Add Patient")');
    await page.fill('input[name="name"]', 'Yang Jun\'ai');
    await page.selectOption('select[name="language"]', 'ZH');
    await page.fill('input[name="contact_info"]', 'yang@example.com');
    await page.click('button:has-text("Save")');

    // Register third patient
    await page.click('button:has-text("Add Patient")');
    await page.fill('input[name="name"]', 'Jiang Yihui');
    await page.selectOption('select[name="language"]', 'ZH');
    await page.fill('input[name="contact_info"]', 'jiang@example.com');
    await page.click('button:has-text("Save")');

    // Step 2: Group Appointment Coordination
    await page.goto('/appointments');

    // Book appointments for group using the Add Appointment button
    // Huang Jia-yi and Yang Jun'ai together at 10:00
    await page.click('button:has-text("Add Appointment")');
    await page.selectOption('select[name="patient"]', { label: 'Huang Jia-yi' });
    await page.selectOption('select[name="doctor"]', { label: 'Dr. Kim' });
    await page.fill('input[type="date"]', '2025-03-06');
    await page.fill('input[type="time"]', '10:00');
    await page.click('button:has-text("Book")');

    await page.click('button:has-text("Add Appointment")');
    await page.selectOption('select[name="patient"]', { label: 'Yang Jun\'ai' });
    await page.selectOption('select[name="doctor"]', { label: 'Dr. Kim' });
    await page.fill('input[type="date"]', '2025-03-06');
    await page.fill('input[type="time"]', '10:00');
    await page.click('button:has-text("Book")');

    // Jiang Yihui at 11:30
    await page.click('button:has-text("Add Appointment")');
    await page.selectOption('select[name="patient"]', { label: 'Jiang Yihui' });
    await page.selectOption('select[name="doctor"]', { label: 'Dr. Park' });
    await page.fill('input[type="date"]', '2025-03-06');
    await page.fill('input[type="time"]', '11:30');
    await page.click('button:has-text("Book")');

    // Verify appointments appear
    await expect(page.locator('text=Huang Jia-yi')).toBeVisible();
    await expect(page.locator('text=Yang Jun\'ai')).toBeVisible();
    await expect(page.locator('text=Jiang Yihui')).toBeVisible();

    // Step 3: Price Inquiry Management
    await page.goto('/messages');
    await page.click('text=Huang Jia-yi');

    // Provide pricing information
    await page.fill('input[placeholder*="message"]', 'Botox: 990,000 KRW for jaw muscle. Hyaluronic acid: 1,650,000 KRW per cc');
    await page.click('button[type="submit"]');

    // Verify pricing message sent
    await expect(page.locator('text=Botox:')).toBeVisible();

    // Step 4: Post-Treatment Instructions
    // After treatment completion, send post-treatment care instructions
    await page.goto('/patients');
    await page.click('text=Huang Jia-yi');

    // Send post-treatment instructions
    await page.fill('textarea[name="notes"]', 'Post-treatment care instructions');
    await page.click('button:has-text("Save")');

    await expect(page.locator('text=Success')).toBeVisible();
  });

  // Test scenario 3: Regular Workflow
  test('Scenario 3: Regular Workflow', async ({ page }) => {
    // Navigate to dashboard (already authenticated)
    await page.goto('/');

    // Daily Patient Communication
    await page.goto('/messages');
    await expect(page.locator('h2')).toContainText('messages.conversationList'); // Should show messages page

    // Appointment Management
    await page.goto('/appointments');
    await expect(page.locator('h1')).toContainText('staff.appointments.title'); // Should show appointments page

    // Filter by doctor, patient language, or appointment status
    await page.selectOption('select[name="doctor"]', 'Dr. Jung Nam-ju');
    await page.selectOption('select[name="language"]', 'JA');
    await page.selectOption('select[name="status"]', 'PENDING');

    // Patient Record Management
    await page.goto('/patients');

    // Sort by language preference
    await page.click('text=Language');

    // Update patient contact information
    await page.click('text=Edit');
    await page.fill('input[name="contact_info"]', 'updated@example.com');
    await page.click('button:has-text("Save")');

    await expect(page.locator('text=Success')).toBeVisible();
  });
});