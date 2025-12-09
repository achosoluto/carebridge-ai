import { test, expect } from '@playwright/test';

test.describe('Chatlog Scenario Testing', () => {
  // Test the Japanese consultation scenario
  test('Japanese Nose Consultation Scenario', async ({ request }) => {
    const baseURL = process.env.VITE_API_BASE_URL || 'http://localhost:8000';

    console.log('Testing Japanese consultation scenario...');

    // Patient's first message: "はじめまして。鼻のカウンセリングを検討しております。11月5日16:00以降で空いている時間はありますでしょうか?"
    const response1 = await request.post(`${baseURL}/chatbot/message/`, {
      data: { message: 'はじめまして。鼻のカウンセリングを検討しております。11月5日16:00以降で空いている時間はありますでしょうか?' }
    });

    expect(response1.ok()).toBeTruthy();
    const data1 = await response1.json();
    console.log('Bot response to Japanese inquiry:', data1.response);

    // The current bot only does English keyword matching, so it will likely give a generic response
    // In a real scenario, this should be handled by staff, not the bot

    // Test a few more messages from the log
    const messages = [
      '1.年内 2.チョンナムジュ院長 3.唇フィラー等あり(手術はありません) 4.Twitter よろしくお願いいたします。',
      '11月5日17:00でよろしくお願いいたします。 通訳者を連れていくことが難しいのですが大丈夫でしょうか?',
      'NAK********* 当日はどうぞよろしくお願いいたします。',
      'お世話になっております。11月5日17:00予約させていただいているのですが、14:00頃に変更は可能でしょうか?',
      'お世話になっております。 ご対応いただき誠にありがとうございます。 5時から2時への変更、確かに承知いたしました。 お手数をおかけしますが、何卒よろしくお願いいたします。',
      'お世話になっております。 明日予定通りに伺います。どうぞよろしくお願いいたします。'
    ];

    for (const message of messages) {
      const response = await request.post(`${baseURL}/chatbot/message/`, {
        data: { message: message }
      });
      expect(response.ok()).toBeTruthy();
      const data = await response.json();
      console.log(`Message: "${message.substring(0, 50)}..."`);
      console.log(`Bot response: "${data.response}"`);
      console.log('---');
    }
  });

  // Test the Chinese group consultation scenario
  test('Chinese Group Consultation Scenario', async ({ request }) => {
    const baseURL = process.env.VITE_API_BASE_URL || 'http://localhost:8000';

    console.log('Testing Chinese group consultation scenario...');

    // Initial inquiry: "您好 想請問 咀嚼肌肉毒、嘴唇玻尿酸 、美版超聲刀 的價錢，謝謝🙏"
    const response1 = await request.post(`${baseURL}/chatbot/message/`, {
      data: { message: '您好 想請問 咀嚼肌肉毒、嘴唇玻尿酸 、美版超聲刀 的價錢，謝謝🙏' }
    });

    expect(response1.ok()).toBeTruthy();
    const data1 = await response1.json();
    console.log('Bot response to Chinese pricing inquiry:', data1.response);

    // Test more messages from the Chinese chatlog
    const messages = [
      '好的謝謝，請問有美版音波嗎🤩',
      '了解😊 請問諮詢的話是諮詢師看完後院長會再評估一次嗎？中文服務都會陪同整個過程嗎🥹 謝謝🙏',
      '好的😆 我想預約3/7 早上10:30  3位 謝謝🙏',
      '另外想請問單純打咀嚼肌肉毒 費用是多少呢？ 有分品牌嗎？謝謝',
      '好的～謝謝！',
      '請問韓版的維持時間大約多久呢🥹',
      '好的 謝謝(感謝)',
      '想再請問 你們有Onda嗎🥹',
      '好的～謝謝！',
      '想再請問你們喬雅登的費用～謝謝！',
      '請問韓版的維持時間大約多久呢🥹',
      '好的 謝謝(感謝)',
      '想再請問 你們有Onda嗎🥹',
      '好的～謝謝！',
      '您好，想請問今年11月還有空檔可以預約嗎？兩位',
      '11/10-11/22期間有空檔嗎',
      '請問11/13可以預約兩位嗎？謝謝',
      '您好 可以，麻煩您了',
      '好的 謝謝(感謝)',
      '您好 請問費用如何計算呢 謝謝',
      '腋下止汗肉毒素',
      '您好，想確認我們明天10點的預約',
      '謝謝，明天見'
    ];

    for (const message of messages) {
      const response = await request.post(`${baseURL}/chatbot/message/`, {
        data: { message: message }
      });
      expect(response.ok()).toBeTruthy();
      const data = await response.json();
      console.log(`Message: "${message.substring(0, 50)}..."`);
      console.log(`Bot response: "${data.response}"`);
      console.log('---');
    }
  });

  // Test English keywords that should trigger responses
  test('English Keyword Responses', async ({ request }) => {
    const baseURL = process.env.VITE_API_BASE_URL || 'http://localhost:8000';

    console.log('Testing English keyword responses...');

    const testCases = [
      { message: 'What are your opening hours?', expectedContains: 'open from 9 AM to 5 PM' },
      { message: 'Where is the clinic located?', expectedContains: 'located at 123 Health St' },
      { message: 'How do I book an appointment?', expectedContains: 'book an appointment by calling' },
      { message: 'What services do you offer?', expectedContains: 'range of services' },
      { message: 'I need help with something else', expectedContains: 'don\'t understand' }
    ];

    for (const testCase of testCases) {
      const response = await request.post(`${baseURL}/chatbot/message/`, {
        data: { message: testCase.message }
      });
      expect(response.ok()).toBeTruthy();
      const data = await response.json();
      console.log(`Input: "${testCase.message}"`);
      console.log(`Response: "${data.response}"`);
      expect(data.response).toContain(testCase.expectedContains);
      console.log('✓ Matched expected response');
      console.log('---');
    }
  });
});