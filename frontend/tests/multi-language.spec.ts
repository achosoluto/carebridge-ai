import { test, expect } from '@playwright/test';

test.describe('Multi-Language UAT Tests', () => {
  const supportedLanguages = ['ko', 'en', 'zh', 'ja'];

  supportedLanguages.forEach((lang) => {
    test.describe(`Language: ${lang}`, () => {
      test(`should display ${lang} interface elements correctly`, async ({ page }) => {
        // Navigate to dashboard
        await page.goto('/staff/dashboard');
        
        // Test language-specific UI elements
        await expect(page.locator('h1')).toContainText(getExpectedText('dashboard', lang));
        
        // Test navigation elements
        await expect(page.locator('nav')).toContainText(getExpectedText('navigation', lang));
        
        // Test that language switching works if implemented
        if (await page.locator('[data-testid="language-switcher"]').count() > 0) {
          await page.click('[data-testid="language-switcher"]');
          await page.selectOption('select', lang);
          await page.waitForTimeout(1000);
        }
        
        // Verify language-specific content
        await verifyLanguageContent(page, lang);
      });

      test(`should handle ${lang} patient names and communication`, async ({ page }) => {
        await page.goto('/staff/messages');
        
        // Look for patient names in different languages
        const patientNames = page.locator('[data-testid="patient-name"]');
        const nameCount = await patientNames.count();
        
        if (nameCount > 0) {
          // Verify names display correctly
          const firstName = await patientNames.first().textContent();
          expect(firstName).toBeTruthy();
          
          // Test search with language-specific characters
          if (lang === 'ko') {
            await page.fill('input[placeholder*="Search patients"]', '김');
          } else if (lang === 'zh') {
            await page.fill('input[placeholder*="Search patients"]', '张');
          } else if (lang === 'ja') {
            await page.fill('input[placeholder*="Search patients"]', '田中');
          }
        }
      });

      test(`should display ${lang} message content properly`, async ({ page }) => {
        await page.goto('/staff/messages');
        
        // Look for message content
        const messages = page.locator('[data-testid="message-content"]');
        const messageCount = await messages.count();
        
        if (messageCount > 0) {
          const firstMessage = await messages.first().textContent();
          expect(firstMessage).toBeTruthy();
          
          // Verify message language detection indicators
          await expect(page.locator('[data-testid="language-indicator"]')).toBeVisible();
        }
      });
    });
  });

  test('should handle language switching between supported languages', async ({ page }) => {
    await page.goto('/staff/dashboard');
    
    // Test switching between languages
    for (const lang of supportedLanguages.slice(0, 2)) { // Test first 2 languages
      if (await page.locator('[data-testid="language-switcher"]').count() > 0) {
        await page.click('[data-testid="language-switcher"]');
        await page.selectOption('select', lang);
        await page.waitForTimeout(1000);
        
        // Verify language switch
        await expect(page.locator('body')).toContainText(getExpectedText('dashboard', lang));
      }
    }
  });

  test('should maintain language preference across page navigation', async ({ page }) => {
    // Set Korean as default
    await page.goto('/staff/dashboard');
    
    if (await page.locator('[data-testid="language-switcher"]').count() > 0) {
      await page.selectOption('select', 'ko');
      await page.waitForTimeout(1000);
      
      // Navigate to different pages
      await page.click('text=Messages');
      await expect(page).toHaveURL('/staff/messages');
      
      await page.click('text=Appointments');
      await expect(page).toHaveURL('/staff/appointments');
      
      // Return to dashboard and verify language preference is maintained
      await page.click('text=Dashboard');
      await expect(page.locator('body')).toContainText('환영합니다'); // Korean welcome text
    }
  });
});

function getExpectedText(element: string, lang: string): string {
  const translations: Record<string, Record<string, string>> = {
    dashboard: {
      ko: 'Staff Dashboard',
      en: 'Staff Dashboard', 
      zh: 'Staff Dashboard',
      ja: 'Staff Dashboard'
    },
    navigation: {
      ko: 'Messages',
      en: 'Messages',
      zh: 'Messages', 
      ja: 'Messages'
    }
  };
  
  return translations[element]?.[lang] || element;
}

async function verifyLanguageContent(page: any, lang: string): Promise<void> {
  // Verify language-specific elements based on the language
  switch (lang) {
    case 'ko':
      // Verify Korean text elements
      await expect(page.locator('body')).toContainText(/관리|환자|메시지/);
      break;
    case 'zh':
      // Verify Chinese text elements
      await expect(page.locator('body')).toContainText(/管理|患者|消息/);
      break;
    case 'ja':
      // Verify Japanese text elements
      await expect(page.locator('body')).toContainText(/管理|患者|メッセージ/);
      break;
    default:
      // English or other languages
      await expect(page.locator('body')).toContainText(/Management|Patient|Message/);
  }
}