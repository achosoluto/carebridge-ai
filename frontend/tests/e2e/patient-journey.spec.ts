import { test, expect } from '@playwright/test';

test.describe('Patient Journey', () => {
  test('should allow patient to visit website and navigate to booking', async ({ page }) => {
    // 1. Patient visits clinic website
    await page.goto('/portal');

    // Verify we're on the portal home page
    await expect(page).toHaveURL(/.*portal$/);
    // Wait for page to load and check for welcome message
    await expect(page.locator('h1').first()).toBeVisible();

    // 2. Navigate to booking page using href selector for better Firefox compatibility
    await page.click('a[href="/portal/book"]');

    // 3. Verify we're on the booking page
    await expect(page).toHaveURL(/.*portal\/book$/);
    await expect(page.locator('h1').filter({ hasText: '예약하기' })).toBeVisible();

    // 4. Check if doctors are available
    const doctorCards = page.locator('.grid.grid-cols-1.sm\\:grid-cols-2 > div');

    if (await doctorCards.count() > 0) {
      // If doctors are available, test the full booking flow
      await doctorCards.first().click();

      // Fill date and time
      const tomorrow = new Date();
      tomorrow.setDate(tomorrow.getDate() + 1);
      const dateString = tomorrow.toISOString().split('T')[0];

      await page.fill('input[type="date"]', dateString);
      await page.fill('input[type="time"]', '10:00');

      // Fill patient details
      await page.fill('input[placeholder*="홍길동"]', 'Test Patient');
      await page.fill('input[placeholder*="연락처"]', 'test@example.com');

      // Select Japanese language
      await page.selectOption('select', 'JA');

      // Submit booking
      await page.click('text=예약 확인');

      // Verify confirmation page
      await expect(page.locator('text=예약 확인됨!')).toBeVisible();
    } else {
      // If no doctors are available, just verify the form loads
      console.log('No doctors available - testing basic form loading');
      await expect(page.locator('input[placeholder*="홍길동"]')).toBeVisible();
      await expect(page.locator('input[type="date"]')).toBeVisible();
      await expect(page.locator('input[type="time"]')).toBeVisible();
    }
  });

  test('should handle booking validation', async ({ page }) => {
    await page.goto('/portal/book');

    // Wait for page to load with longer timeout for Firefox
    await page.waitForSelector('input[placeholder*="홍길동"]', { timeout: 30000 });

    // Fill required fields but don't select a doctor
    await page.fill('input[placeholder*="홍길동"]', 'Test Patient');
    await page.fill('input[placeholder*="연락처"]', 'test@example.com');

    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    const dateString = tomorrow.toISOString().split('T')[0];

    await page.fill('input[type="date"]', dateString);
    await page.fill('input[type="time"]', '10:00');

    // Button should be disabled since no doctor is selected
    await expect(page.locator('button[type="submit"]')).toBeDisabled();
  });
});