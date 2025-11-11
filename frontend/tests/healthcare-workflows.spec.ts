import { test, expect } from '@playwright/test';

test.describe('Healthcare Workflow UAT Tests', () => {
  test.describe('Patient Management Workflows', () => {
    test.beforeEach(async ({ page }) => {
      // Ensure we're logged in and on dashboard
      await page.goto('/staff/dashboard');
    });

    test('should view patient details and communication history', async ({ page }) => {
      // Navigate to messages page
      await page.click('text=Messages');
      await page.waitForURL('/staff/messages');
      
      // Wait for patient conversations to load
      await page.waitForSelector('[data-testid="conversation-card"]', { timeout: 10000 });
      
      // Click on a patient conversation
      const firstConversation = page.locator('[data-testid="conversation-card"]').first();
      await firstConversation.click();
      
      // Should navigate to patient details
      await expect(page).toHaveURL(/\/staff\/messages\/\d+/);
      
      // Verify patient details are displayed
      await expect(page.locator('h1')).toContainText('Patient Details');
      await expect(page.locator('[data-testid="patient-name"]')).toBeVisible();
      await expect(page.locator('[data-testid="patient-phone"]')).toBeVisible();
    });

    test('should search and filter patient conversations', async ({ page }) => {
      await page.goto('/staff/messages');
      
      // Test search functionality
      const searchInput = page.locator('input[placeholder*="Search patients"]');
      await searchInput.fill('test patient');
      
      // Verify search results update
      await page.waitForTimeout(500);
      
      // Test filter functionality
      const filterSelect = page.locator('select');
      await filterSelect.selectOption('needs-human');
      
      // Verify filtered results
      await expect(page.locator('[data-testid="conversation-card"]')).toHaveCount(0);
      
      // Reset filter
      await filterSelect.selectOption('all');
    });
  });

  test.describe('AI Translation and Communication Workflows', () => {
    test('should display messages with AI confidence scores and language detection', async ({ page }) => {
      await page.goto('/staff/messages');
      
      // Look for messages with AI indicators
      const aiMessages = page.locator('[data-testid="ai-handled-indicator"]');
      
      if (await aiMessages.count() > 0) {
        // Verify AI confidence score is displayed
        await expect(aiMessages.first()).toContainText('AI');
        
        // Verify confidence percentage
        await expect(page.locator('[data-testid="confidence-score"]')).toBeVisible();
      }
    });

    test('should handle multi-language message display', async ({ page }) => {
      await page.goto('/staff/messages');
      
      // Look for language indicators
      const languageFlags = page.locator('[data-testid="language-flag"]');
      
      if (await languageFlags.count() > 0) {
        // Verify different language flags are displayed
        await expect(languageFlags.first()).toBeVisible();
        
        // Test Korean language display (default)
        await expect(page.locator('body')).toContainText('환영합니다');
      }
    });
  });

  test.describe('Appointment Management Workflows', () => {
    test('should navigate to appointments page and display scheduling interface', async ({ page }) => {
      await page.goto('/staff/appointments');
      
      // Verify appointments page loads
      await expect(page.locator('h1')).toContainText('Appointments');
      
      // Check for appointment scheduling interface
      await expect(page.locator('[data-testid="appointment-calendar"]')).toBeVisible();
      
      // Verify appointment list
      await expect(page.locator('[data-testid="appointment-list"]')).toBeVisible();
    });

    test('should allow appointment creation and management', async ({ page }) => {
      await page.goto('/staff/appointments');
      
      // Click create appointment button
      await page.click('[data-testid="create-appointment-btn"]');
      
      // Fill appointment form
      await page.fill('[data-testid="appointment-patient"]', 'Test Patient');
      await page.fill('[data-testid="appointment-date"]', '2024-01-15');
      await page.fill('[data-testid="appointment-time"]', '10:00');
      
      // Submit form
      await page.click('[data-testid="save-appointment"]');
      
      // Verify appointment was created
      await expect(page.locator('[data-testid="success-message"]')).toContainText('success');
    });
  });

  test.describe('System Monitoring Workflows', () => {
    test('should display system metrics and performance data', async ({ page }) => {
      await page.goto('/staff/monitoring');
      
      // Verify monitoring dashboard loads
      await expect(page.locator('h1')).toContainText('System Monitoring');
      
      // Check for performance metrics
      await expect(page.locator('[data-testid="ai-accuracy"]')).toBeVisible();
      await expect(page.locator('[data-testid="response-time"]')).toBeVisible();
      await expect(page.locator('[data-testid="uptime"]')).toBeVisible();
      
      // Verify channel status indicators
      await expect(page.locator('[data-testid="channel-status"]')).toBeVisible();
    });

    test('should display real-time connection status', async ({ page }) => {
      await page.goto('/staff/dashboard');
      
      // Look for connection status indicator
      const connectionStatus = page.locator('[data-testid="connection-status"]');
      await expect(connectionStatus).toBeVisible();
      
      // Verify connection status text
      await expect(connectionStatus).toContainText(/Connected|Disconnected/);
    });
  });
});