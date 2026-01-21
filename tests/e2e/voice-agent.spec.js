/**
 * E2E tests for voice agent web application.
 * Tests complete user workflows using Playwright.
 */

import { test, expect } from '@playwright/test';

test.describe('Voice Agent - Consult Scheduling', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the app before each test
    await page.goto('http://localhost:3000');
  });

  test('user can schedule a consult through the form', async ({ page }) => {
    // Navigate to scheduling page
    await page.click('[data-testid="schedule-consult-button"]');
    
    // Fill in the form
    await page.fill('[data-testid="name-input"]', 'John Doe');
    await page.fill('[data-testid="email-input"]', 'john.doe@example.com');
    await page.fill('[data-testid="phone-input"]', '+1234567890');
    
    // Select a date (assuming a date picker)
    await page.click('[data-testid="date-picker"]');
    await page.click('text=15'); // Select day 15
    
    // Select time
    await page.selectOption('[data-testid="time-select"]', '10:00 AM');
    
    // Submit the form
    await page.click('[data-testid="submit-consult-button"]');
    
    // Verify success message
    await expect(page.locator('[data-testid="success-message"]')).toBeVisible();
    await expect(page.locator('[data-testid="success-message"]')).toContainText('scheduled');
  });

  test('form validation prevents submission with invalid email', async ({ page }) => {
    await page.click('[data-testid="schedule-consult-button"]');
    
    await page.fill('[data-testid="name-input"]', 'John Doe');
    await page.fill('[data-testid="email-input"]', 'invalid-email'); // Invalid email
    await page.fill('[data-testid="phone-input"]', '+1234567890');
    
    await page.click('[data-testid="submit-consult-button"]');
    
    // Verify error message
    await expect(page.locator('[data-testid="email-error"]')).toBeVisible();
    await expect(page.locator('[data-testid="email-error"]')).toContainText('valid email');
  });

  test('user can view scheduled consults', async ({ page }) => {
    // Navigate to consults page
    await page.click('[data-testid="view-consults-button"]');
    
    // Wait for consults to load
    await page.waitForSelector('[data-testid="consult-list"]');
    
    // Verify consult items are displayed
    const consultItems = page.locator('[data-testid="consult-item"]');
    const count = await consultItems.count();
    
    if (count > 0) {
      // Verify first consult has required fields
      await expect(consultItems.first().locator('[data-testid="consult-name"]')).toBeVisible();
      await expect(consultItems.first().locator('[data-testid="consult-date"]')).toBeVisible();
    }
  });
});

test.describe('Voice Agent - FAQ Interaction', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000');
  });

  test('user can search FAQs', async ({ page }) => {
    // Navigate to FAQ section
    await page.click('[data-testid="faq-section"]');
    
    // Search for a question
    await page.fill('[data-testid="faq-search-input"]', 'hours');
    await page.press('[data-testid="faq-search-input"]', 'Enter');
    
    // Wait for results
    await page.waitForSelector('[data-testid="faq-results"]');
    
    // Verify results are displayed
    const results = page.locator('[data-testid="faq-item"]');
    await expect(results.first()).toBeVisible();
  });

  test('user can expand FAQ to see answer', async ({ page }) => {
    await page.click('[data-testid="faq-section"]');
    
    // Click on first FAQ item
    const firstFaq = page.locator('[data-testid="faq-item"]').first();
    await firstFaq.click();
    
    // Verify answer is visible
    await expect(firstFaq.locator('[data-testid="faq-answer"]')).toBeVisible();
  });
});

test.describe('Voice Agent - Voice Interaction', () => {
  test.beforeEach(async ({ page, context }) => {
    // Mock getUserMedia for voice recording
    await context.grantPermissions(['microphone']);
    
    await page.addInitScript(() => {
      // Mock MediaRecorder
      window.MediaRecorder = class MockMediaRecorder {
        constructor(stream) {
          this.stream = stream;
          this.state = 'inactive';
        }
        start() {
          this.state = 'recording';
        }
        stop() {
          this.state = 'inactive';
        }
        addEventListener() {}
      };
      
      // Mock getUserMedia
      navigator.mediaDevices.getUserMedia = async () => {
        return new MediaStream();
      };
    });
    
    await page.goto('http://localhost:3000');
  });

  test('user can start voice recording', async ({ page }) => {
    // Navigate to voice chat
    await page.click('[data-testid="voice-chat-button"]');
    
    // Click start recording
    await page.click('[data-testid="start-recording-button"]');
    
    // Verify recording indicator is visible
    await expect(page.locator('[data-testid="recording-indicator"]')).toBeVisible();
    await expect(page.locator('[data-testid="recording-indicator"]')).toContainText('Recording');
  });

  test('user can stop recording and see transcription', async ({ page }) => {
    await page.click('[data-testid="voice-chat-button"]');
    await page.click('[data-testid="start-recording-button"]');
    
    // Wait a moment (simulating recording)
    await page.waitForTimeout(1000);
    
    // Stop recording
    await page.click('[data-testid="stop-recording-button"]');
    
    // Verify transcription appears
    await expect(page.locator('[data-testid="transcription-text"]')).toBeVisible({ timeout: 5000 });
  });

  test('user receives voice response after asking question', async ({ page }) => {
    await page.click('[data-testid="voice-chat-button"]');
    
    // Mock the voice processing response
    await page.route('**/api/voice/process', route => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          response: 'Our hours are Monday through Friday, 9 AM to 5 PM EST.',
          audio_url: '/mock-audio-response.mp3'
        })
      });
    });
    
    // Simulate asking a question
    await page.fill('[data-testid="voice-input"]', 'What are your hours?');
    await page.click('[data-testid="send-voice-message-button"]');
    
    // Verify response appears
    await expect(page.locator('[data-testid="voice-response"]')).toBeVisible({ timeout: 5000 });
    await expect(page.locator('[data-testid="voice-response"]')).toContainText('9 AM to 5 PM');
  });
});

test.describe('Voice Agent - Responsive Design', () => {
  test('app works on mobile viewport', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('http://localhost:3000');
    
    // Verify mobile menu is accessible
    const menuButton = page.locator('[data-testid="mobile-menu-button"]');
    if (await menuButton.isVisible()) {
      await menuButton.click();
      await expect(page.locator('[data-testid="mobile-menu"]')).toBeVisible();
    }
  });

  test('app works on tablet viewport', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto('http://localhost:3000');
    
    // Verify layout adapts
    await expect(page.locator('body')).toBeVisible();
  });
});
