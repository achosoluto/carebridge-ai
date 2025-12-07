import { test, expect } from '@playwright/test';

test.describe('Staff Journey', () => {
  test('should allow staff to login and access dashboard', async ({ page }) => {
    // 1. Staff logs into simple dashboard
    await page.goto('/login');

    // Fill login form
    await page.fill('input[type="text"]', 'testuser');
    await page.fill('input[type="password"]', 'testpass');

    // Submit login
    await page.click('button[type="submit"]');

    // Should redirect to dashboard
    await expect(page).toHaveURL(/.*\/$/);
    await expect(page.locator('nav')).toBeVisible();
  });

  test('should allow staff to view and respond to patient messages', async ({ page }) => {
    // Login first
    await page.goto('/login');
    await page.fill('input[type="text"]', 'testuser');
    await page.fill('input[type="password"]', 'testpass');
    await page.click('button[type="submit"]');

    // Navigate to messages
    await page.goto('/messages');

    // Verify messages interface loads
    await expect(page.locator('text=Conversation List')).toBeVisible();

    // If there are patients, select one
    const patientList = page.locator('.divide-y.divide-gray-100');
    // Wait for the container to be visible first for better Firefox compatibility
    await expect(patientList).toBeVisible();
    const count = await patientList.count();
    if (count > 0) {
      await patientList.first().click();

      // Verify chat area appears
      await expect(page.locator('text=Enter message (Korean)...')).toBeVisible();

      // Type a message in Korean
      await page.fill('input[placeholder*="Enter message (Korean)..."]', '안녕하세요, 어떻게 도와드릴까요?');

      // Send message
      await page.click('button[type="submit"]');

      // Message should appear in chat
      await expect(page.locator('text=안녕하세요, 어떻게 도와드릴까요?')).toBeVisible();
    } else {
      // No patients, just verify interface
      await expect(page.locator('text=Select a patient')).toBeVisible();
    }
  });

  test('should allow staff to manage appointments', async ({ page }) => {
    // Login first
    await page.goto('/login');
    await page.fill('input[type="text"]', 'testuser');
    await page.fill('input[type="password"]', 'testpass');
    await page.click('button[type="submit"]');

    // Navigate to appointments
    await page.goto('/appointments');

    // Verify appointments interface loads
    await expect(page.locator('h2').filter({ hasText: 'Appointment Management' })).toBeVisible();
  });

  test('should handle navigation between staff sections', async ({ page }) => {
    // Login first
    await page.goto('/login');
    await page.fill('input[type="text"]', 'testuser');
    await page.fill('input[type="password"]', 'testpass');
    await page.click('button[type="submit"]');

    // Test navigation to different sections
    await page.goto('/messages');
    await expect(page).toHaveURL(/.*messages$/);

    await page.goto('/appointments');
    await expect(page).toHaveURL(/.*appointments$/);

    await page.goto('/patients');
    await expect(page).toHaveURL(/.*patients$/);

    await page.goto('/');
    await expect(page).toHaveURL(/.*\/$/);
  });
});