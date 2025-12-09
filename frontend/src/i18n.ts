import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

import enTranslations from './locales/en.json';
import koTranslations from './locales/ko.json';
import jaTranslations from './locales/ja.json';
import zhTranslations from './locales/zh.json';

// Simplified language detection
const detectLanguage = () => {
  // 1. Explicit user selection (highest priority)
  const saved = localStorage.getItem('language');
  if (saved && ['en', 'ko', 'ja', 'zh'].includes(saved)) return saved;

  // 2. User profile (when authenticated)
  // TODO: Fetch from API when user logs in

  // 3. Browser detection (lowest priority)
  const browserLang = navigator.language.split('-')[0];
  return ['en', 'ko', 'ja', 'zh'].includes(browserLang) ? browserLang : 'en';
};

i18n
  .use(initReactI18next)
  .init({
    resources: {
      en: {
        translation: enTranslations,
      },
      ko: {
        translation: koTranslations,
      },
      ja: {
        translation: jaTranslations,
      },
      zh: {
        translation: zhTranslations,
      },
    },
    lng: detectLanguage(), // Use detected language
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false,
    },
    react: {
      useSuspense: false // Fixes issues with translation loading
    }
  });

export default i18n;