# CareBridge AI - Automated Browser-Based UAT Testing Guide

## Overview

This guide provides comprehensive information about implementing automated browser-based UAT testing for the CareBridge AI healthcare platform using Playwright.

## 🎯 Recommended Solution: Playwright

### Why Playwright?

After evaluating available tools, **Playwright** is the recommended solution for CareBridge AI because:

1. **Modern JavaScript/TypeScript Support**: Native TypeScript support aligns with existing frontend stack
2. **Cross-Browser Testing**: Supports Chromium, Firefox, and WebKit for comprehensive coverage
3. **Mobile Testing**: Built-in device emulation for responsive healthcare workflows
4. **Auto-Waiting**: Intelligent element detection reduces flakiness in healthcare workflows
5. **Multi-Language Support**: Excellent support for Korean, Chinese, Japanese character testing
6. **API Integration**: Direct integration with Django backend testing
7. **Screenshots & Videos**: Automatic capture for debugging healthcare scenarios

## 🚀 Quick Start Implementation

### Prerequisites
- Node.js 16+ installed
- CareBridge AI frontend running on `http://localhost:5173`
- CareBridge AI backend running on `http://localhost:8000`

### Installation Commands

```bash
# Navigate to frontend directory
cd frontend

# Install Playwright (already completed)
npm install --save-dev playwright @playwright/test

# Install browser binaries (already completed)
npx playwright install

# Verify installation
npx playwright --version
```

### Test Scripts Available

```bash
# Run all tests
npm test

# Run tests with UI mode
npm run test:ui

# Run tests in headed mode (visible browser)
npm run test:headed

# Debug tests
npm run test:debug

# View test report
npm run test:report
```

## 📋 Test Structure

### Current Test Coverage

```
tests/
├── example.spec.ts                    # Basic functionality tests
├── healthcare-workflows.spec.ts       # Core healthcare workflows
├── multi-language.spec.ts            # Multi-language support testing
└── utils/
    └── test-helpers.ts               # Reusable test utilities
```

### Healthcare Workflows Covered

1. **Patient Management**
   - Patient conversation viewing
   - Communication history
   - Search and filtering

2. **AI Translation & Communication**
   - Confidence score display
   - Language detection
   - Multi-language message handling

3. **Appointment Management**
   - Appointment scheduling
   - Calendar interface
   - Appointment creation/management

4. **System Monitoring**
   - Performance metrics
   - Real-time connection status
   - Channel status indicators

## 🌍 Multi-Language Testing

### Supported Languages
- Korean (ko) - Primary language
- English (en)
- Chinese (zh)
- Japanese (ja)

### Test Coverage
- UI element translation verification
- Patient name handling in different scripts
- Message content display
- Language preference persistence
- Search functionality with non-ASCII characters

## 🔧 Integration with Development Workflow

### CI/CD Integration

Add to your GitHub Actions workflow (`.github/workflows/uat-tests.yml`):

```yaml
name: UAT Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-node@v3
      with:
        node-version: '18'
    - run: cd frontend && npm install
    - run: cd frontend && npx playwright install
    - run: cd frontend && npm test
```

### Development Integration

1. **Pre-commit Hooks**: Run subset of tests before committing
2. **Local Development**: Use `npm run test:ui` for interactive testing
3. **Staging Environment**: Configure separate test environments

## 📊 Test Results and Reporting

### HTML Reports
- Generated in `playwright-report/`
- Screenshots and videos for failed tests
- Detailed test execution timeline

### Healthcare-Specific Metrics
- Patient workflow completion rates
- Multi-language test coverage
- API response times
- Real-time connection reliability

## 🛠️ Advanced Testing Features

### Accessibility Testing
```typescript
// Example accessibility test
test('should meet accessibility standards', async ({ page }) => {
  await page.goto('/staff/dashboard');
  
  // Add axe-core integration for accessibility testing
  const accessibilityScanResults = await new AxePuppeteer(page).analyze();
  expect(accessibilityScanResults.violations).toEqual([]);
});
```

### Performance Testing
```typescript
// Example performance test
test('should load dashboard within acceptable time', async ({ page }) => {
  const startTime = Date.now();
  await page.goto('/staff/dashboard');
  await page.waitForLoadState('networkidle');
  
  const loadTime = Date.now() - startTime;
  expect(loadTime).toBeLessThan(3000); // 3 second threshold
});
```

### API Integration Testing
```typescript
// Example API test
test('should communicate with Django backend', async ({ page }) => {
  await page.goto('/staff/messages');
  
  // Intercept API calls
  const response = await page.waitForResponse(
    response => response.url().includes('/api/') && response.status() === 200
  );
  
  expect(response.ok()).toBeTruthy();
});
```

## 🏥 Healthcare-Specific Test Data

### Test Data Generator
```typescript
import { TestDataGenerator } from './utils/test-helpers';

// Generate realistic healthcare test data
const patientData = TestDataGenerator.generatePatientData();
const appointmentData = TestDataGenerator.generateAppointmentData();
const messageData = TestDataGenerator.generateMessageData();
```

### Mock Healthcare Scenarios
- Emergency triage situations
- Multi-language patient communications
- High-volume message handling
- AI confidence threshold testing
- Human handoff scenarios

## 📈 Next Steps for Implementation

### Phase 1: Basic Setup (Week 1)
1. ✅ Playwright installation and configuration
2. ✅ Basic test structure creation
3. ⏳ Core workflow test implementation
4. ⏳ Multi-language test development

### Phase 2: Comprehensive Coverage (Week 2-3)
1. ⏳ Complete healthcare workflow testing
2. ⏳ Performance and accessibility testing
3. ⏳ Mobile responsive testing
4. ⏳ Error handling and edge cases

### Phase 3: CI/CD Integration (Week 3-4)
1. ⏳ GitHub Actions workflow setup
2. ⏳ Test environment configuration
3. ⏳ Automated reporting
4. ⏳ Test data management

## 🔍 Troubleshooting

### Common Issues

1. **Frontend not loading**: Ensure `npm run dev` is running
2. **Backend API errors**: Verify Django server is running on port 8000
3. **Element not found**: Use Playwright's auto-waiting features
4. **Flaky tests**: Implement proper waits and retries

### Debug Commands
```bash
# Debug specific test file
npx playwright test healthcare-workflows.spec.ts --debug

# Debug with browser visible
npm run test:headed

# Generate test artifacts
npm test -- --reporter=html
```

## 📚 Additional Resources

- [Playwright Documentation](https://playwright.dev/)
- [CareBridge AI Architecture](./../CAREbridge_AI_SYSTEM_ARCHITECTURE.md)
- [UAT Readiness Assessment](./../CareBridge_AI_UAT_Readiness_Assessment.md)
- [Phase 2 Implementation Guide](./../PHASE_2_IMPLEMENTATION_SUMMARY.md)

## 📞 Support

For questions about UAT testing implementation:
- Review existing test files in `tests/` directory
- Check Playwright documentation for advanced features
- Consult healthcare workflow documentation for domain-specific test cases

---

*This UAT testing framework ensures comprehensive validation of CareBridge AI's healthcare workflows, multi-language support, and integration with the Django backend.*