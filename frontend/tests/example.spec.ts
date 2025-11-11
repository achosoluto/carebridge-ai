import { test, expect } from '@playwright/test';

test.describe('CareBridge AI UAT Tests', () => {
  test('should load the dashboard and display staff interface', async ({ page }) => {
    await page.goto('/');
    
    // Wait for redirect to dashboard
    await page.waitForURL('/staff/dashboard');
    
    // Check if dashboard loads correctly
    await expect(page.locator('h1')).toContainText('Staff Dashboard');
    
    // Verify connection status indicator
    await expect(page.locator('[data-testid="connection-status"]')).toBeVisible();
    
    // Check navigation elements
    await expect(page.locator('nav')).toContainText('Messages');
    await expect(page.locator('nav')).toContainText('Appointments');
    await expect(page.locator('nav')).toContainText('Monitoring');
  });

  test('should navigate to messages page and display patient conversations', async ({ page }) => {
    await page.goto('/staff/dashboard');
    
    // Click on Messages navigation
    await page.click('text=Messages');
    
    // Wait for navigation
    await page.waitForURL('/staff/messages');
    
    // Check if messages page loads
    await expect(page.locator('h1')).toContainText('Patient Messages');
    
    // Verify search functionality is present
    await expect(page.locator('input[placeholder*="Search patients"]')).toBeVisible();
    
    // Verify filter functionality
    await expect(page.locator('select')).toContainText('All Conversations');
  });

  test('should test mobile responsiveness', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    
    await page.goto('/staff/dashboard');
    
    // Check mobile navigation
    await expect(page.locator('button[aria-label="Open menu"]')).toBeVisible();
    
    // Open mobile menu
    await page.click('button[aria-label="Open menu"]');
    
    // Verify mobile menu is open
    await expect(page.locator('[role="dialog"]')).toBeVisible();
  });
});