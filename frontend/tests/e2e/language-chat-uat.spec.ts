import { test, expect } from '@playwright/test';

test.describe('Language Detection and ChatWidget UAT', () => {
  test.beforeEach(async ({ page }) => {
    // Clear localStorage before each test to ensure clean state
    await page.context().addInitScript(() => {
      localStorage.clear();
    });
  });

  test('should detect browser language and show correct default', async ({ page }) => {
    // Set browser language to Japanese
    await page.context().addInitScript(() => {
      Object.defineProperty(navigator, 'language', {
        value: 'ja-JP',
        configurable: true
      });
    });

    await page.goto('/portal');

    // Check that Japanese text appears (welcome message should be in Japanese)
    await expect(page.locator('text=ケアブリッジへようこそ')).toBeVisible();

    // Language selector should show Japanese as selected
    const languageSelect = page.locator('select');
    await expect(languageSelect).toHaveValue('ja');
  });

  test('should allow language switching via UI', async ({ page }) => {
    await page.goto('/portal');

    // Default should be English
    await expect(page.locator('text=Welcome to CareBridge')).toBeVisible();
    const languageSelect = page.locator('select');
    await expect(languageSelect).toHaveValue('en');

    // Change to Korean
    await languageSelect.selectOption('ko');

    // Verify Korean content appears
    await expect(page.locator('text=CareBridge 클리닉에 오신 것을 환영합니다')).toBeVisible();
    await expect(languageSelect).toHaveValue('ko');

    // Change back to English
    await languageSelect.selectOption('en');

    // Verify English content appears
    await expect(page.locator('text=Welcome to CareBridge')).toBeVisible();
    await expect(languageSelect).toHaveValue('en');
  });

  test('should show ChatWidget with correct language', async ({ page }) => {
    await page.goto('/portal');

    // ChatWidget should be visible (bottom right)
    const chatWidget = page.locator('.fixed.bottom-4.right-4');
    await expect(chatWidget).toBeVisible();

    // Should show English chat title by default
    await expect(chatWidget.locator('text=Chat Support')).toBeVisible();

    // Change language to Korean
    const languageSelect = page.locator('select');
    await languageSelect.selectOption('ko');

    // ChatWidget should update to Korean
    await expect(chatWidget.locator('text=채팅 지원')).toBeVisible();
  });

  test('should allow ChatWidget interaction in different languages', async ({ page }) => {
    await page.goto('/portal');

    const chatWidget = page.locator('.fixed.bottom-4.right-4');

    // Change to Chinese
    const languageSelect = page.locator('select');
    await languageSelect.selectOption('zh');

    // ChatWidget should show Chinese
    await expect(chatWidget.locator('text=聊天支持')).toBeVisible();

    // Open chat input
    const chatInput = chatWidget.locator('input[placeholder*="输入您的消息"]');
    await expect(chatInput).toBeVisible();

    // Type a message
    await chatInput.fill('你好');
    await chatInput.press('Enter');

    // Should show user message
    await expect(chatWidget.locator('text=你好')).toBeVisible();

    // Bot response should appear (check for any bot message with white background)
    await expect(chatWidget.locator('.bg-white.text-gray-800')).toBeVisible();
  });

  test('should fallback to English for unsupported browser language', async ({ page }) => {
    // Set browser language to unsupported language
    await page.context().addInitScript(() => {
      Object.defineProperty(navigator, 'language', {
        value: 'fr-FR',
        configurable: true
      });
    });

    await page.goto('/portal');

    // Should default to English
    await expect(page.locator('text=Welcome to CareBridge')).toBeVisible();

    const languageSelect = page.locator('select');
    await expect(languageSelect).toHaveValue('en');
  });

  test('should handle language change during chat session', async ({ page }) => {
    await page.goto('/portal');

    const chatWidget = page.locator('.fixed.bottom-4.right-4');
    const languageSelect = page.locator('select');

    // Start chat in English
    const chatInput = chatWidget.locator('input[placeholder*="Type your message"]');
    await chatInput.fill('Hello');
    await chatInput.press('Enter');

    // Check that the user's message appears (should be in a blue bubble)
    await expect(chatWidget.locator('.bg-blue-500').filter({ hasText: 'Hello' })).toBeVisible();

    // Change language to Japanese during active chat
    await languageSelect.selectOption('ja');

    // Chat input should update to Japanese placeholder
    const japaneseInput = chatWidget.locator('input[placeholder*="入力"]');
    await expect(japaneseInput).toBeVisible();

    // Continue chat in Japanese
    await japaneseInput.fill('こんにちは');
    await japaneseInput.press('Enter');

    await expect(chatWidget.locator('.bg-blue-500').filter({ hasText: 'こんにちは' })).toBeVisible();

    // Previous English message should still be visible (chat history preserved)
    await expect(chatWidget.locator('.bg-blue-500').filter({ hasText: 'Hello' })).toBeVisible();
  });

  test('should not show language switcher in ChatWidget', async ({ page }) => {
    await page.goto('/portal');

    const chatWidget = page.locator('.fixed.bottom-4.right-4');

    // Should NOT have a select dropdown inside the chat widget
    const chatSelects = chatWidget.locator('select');
    await expect(chatSelects).toHaveCount(0);

    // But should have the main language selector in header
    const headerSelect = page.locator('header select');
    await expect(headerSelect).toBeVisible();
  });
});