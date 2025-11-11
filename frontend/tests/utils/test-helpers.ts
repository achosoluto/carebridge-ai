import { Page, BrowserContext, expect } from '@playwright/test';

/**
 * Test utilities for CareBridge AI UAT testing
 */
export class CareBridgeTestHelpers {
  constructor(
    private page: Page,
    private context: BrowserContext
  ) {}

  /**
   * Wait for API response and verify it's successful
   */
  async waitForApiResponse(urlPattern: string, options: { timeout?: number } = {}) {
    const response = await this.page.waitForResponse(
      response => response.url().includes(urlPattern) && response.status() === 200,
      { timeout: options.timeout || 10000 }
    );
    return response;
  }

  /**
   * Fill form fields with validation
   */
  async fillForm(formData: Record<string, string>) {
    for (const [field, value] of Object.entries(formData)) {
      const fieldLocator = this.page.locator(`[data-testid="${field}"], #${field}, [name="${field}"]`);
      await fieldLocator.fill(value);
      await expect(fieldLocator).toHaveValue(value);
    }
  }

  /**
   * Wait for loading states to complete
   */
  async waitForLoading() {
    const loadingElements = this.page.locator('[data-testid="loading"], .loading, .spinner');
    const count = await loadingElements.count();
    
    if (count > 0) {
      await Promise.all([
        this.page.waitForLoadState('networkidle'),
        this.page.waitForFunction(() => {
          const loading = document.querySelector('[data-testid="loading"], .loading, .spinner');
          return !loading || loading.offsetParent === null;
        }, { timeout: 30000 })
      ]);
    }
  }

  /**
   * Navigate to a patient conversation
   */
  async navigateToPatientConversation(patientId?: string) {
    await this.page.click('text=Messages');
    await this.page.waitForURL('/staff/messages');
    await this.waitForLoading();

    if (patientId) {
      await this.page.click(`[data-testid="patient-${patientId}"]`);
    } else {
      // Click first available conversation
      const conversations = this.page.locator('[data-testid="conversation-card"]');
      const count = await conversations.count();
      if (count > 0) {
        await conversations.first().click();
      }
    }
  }

  /**
   * Create a test appointment
   */
  async createTestAppointment(appointmentData: {
    patientName: string;
    date: string;
    time: string;
    type?: string;
  }) {
    await this.page.click('text=Appointments');
    await this.page.waitForURL('/staff/appointments');
    
    await this.page.click('[data-testid="create-appointment-btn"]');
    
    await this.fillForm({
      'appointment-patient': appointmentData.patientName,
      'appointment-date': appointmentData.date,
      'appointment-time': appointmentData.time,
      'appointment-type': appointmentData.type || 'consultation'
    });
    
    await this.page.click('[data-testid="save-appointment"]');
    
    // Verify success
    await expect(this.page.locator('[data-testid="success-message"]')).toBeVisible();
  }

  /**
   * Test real-time connection
   */
  async verifyRealTimeConnection() {
    await this.page.goto('/staff/dashboard');
    
    const connectionStatus = this.page.locator('[data-testid="connection-status"]');
    await expect(connectionStatus).toBeVisible();
    
    const statusText = await connectionStatus.textContent();
    expect(statusText).toMatch(/Connected|Disconnected/);
    
    return statusText?.includes('Connected') || false;
  }

  /**
   * Test accessibility
   */
  async checkAccessibility() {
    // This would require axe-core integration
    const accessibilityScanResults = await this.page.evaluate(async () => {
      // Mock accessibility check
      return { violations: [], passes: [] };
    });
    
    return accessibilityScanResults;
  }

  /**
   * Test responsive design
   */
  async testResponsiveView(width: number, height: number) {
    await this.page.setViewportSize({ width, height });
    await this.page.waitForTimeout(1000);
    
    // Check mobile menu for smaller screens
    if (width < 768) {
      const mobileMenuButton = this.page.locator('button[aria-label="Open menu"]');
      await expect(mobileMenuButton).toBeVisible();
    }
    
    // Reset viewport
    await this.page.setViewportSize({ width: 1920, height: 1080 });
  }

  /**
   * Take screenshot with timestamp
   */
  async takeScreenshot(name: string) {
    await this.page.screenshot({
      path: `test-results/screenshots/${name}-${Date.now()}.png`,
      fullPage: true
    });
  }
}

/**
 * Test data generators for healthcare scenarios
 */
export class TestDataGenerator {
  static generatePatientData() {
    return {
      name: `Test Patient ${Math.floor(Math.random() * 1000)}`,
      phone: `+1-555-${Math.floor(Math.random() * 9000) + 1000}`,
      preferredLanguage: ['ko', 'en', 'zh', 'ja'][Math.floor(Math.random() * 4)],
      age: Math.floor(Math.random() * 80) + 18,
      condition: 'General Consultation'
    };
  }

  static generateAppointmentData() {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    
    return {
      patientName: this.generatePatientData().name,
      date: tomorrow.toISOString().split('T')[0],
      time: `${Math.floor(Math.random() * 12) + 8}:00`,
      type: ['consultation', 'follow-up', 'emergency'][Math.floor(Math.random() * 3)]
    };
  }

  static generateMessageData() {
    const messages = [
      'Hello, I need help with my appointment.',
      'Hi, I have a question about my medication.',
      '계속 아파요. 진료를 예약하고 싶어요.',
      '你好，我想预约看医生。',
      'こんにちは、風邪をひいたかもしれません。'
    ];
    
    return {
      content: messages[Math.floor(Math.random() * messages.length)],
      channel: ['kakao', 'wechat', 'line', 'sms'][Math.floor(Math.random() * 4)],
      direction: Math.random() > 0.5 ? 'incoming' : 'outgoing'
    };
  }
}

/**
 * Environment setup helpers
 */
export class EnvironmentSetup {
  static async setupTestEnvironment(page: Page) {
    // Wait for backend to be ready
    try {
      await page.goto('http://localhost:8000/api/health/', { timeout: 5000 });
      console.log('✅ Backend API is ready');
    } catch (error) {
      console.warn('⚠️ Backend API not available - tests may fail');
    }

    // Wait for frontend to be ready
    await page.goto('http://localhost:5173');
    await page.waitForLoadState('networkidle');
    console.log('✅ Frontend is ready');
  }
}