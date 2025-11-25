import { format, formatDistanceToNow, isToday, isYesterday } from 'date-fns';

// Date formatting utilities
export const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  if (isToday(date)) {
    return `Today ${format(date, 'HH:mm')}`;
  }
  if (isYesterday(date)) {
    return `Yesterday ${format(date, 'HH:mm')}`;
  }
  return format(date, 'MMM d, yyyy HH:mm');
};

export const formatRelativeTime = (dateString: string): string => {
  return formatDistanceToNow(new Date(dateString), { addSuffix: true });
};

// Language utilities
export const getLanguageName = (code: string): string => {
  const languages: Record<string, string> = {
    ko: 'Korean',
    en: 'English',
    zh: 'Chinese',
    ja: 'Japanese',
  };
  return languages[code] || code;
};

export const getLanguageFlag = (code: string): string => {
  const flags: Record<string, string> = {
    ko: '🇰🇷',
    en: '🇺🇸',
    zh: '🇨🇳',
    ja: '🇯🇵',
  };
  return flags[code] || '🌐';
};

// Channel utilities
export const getChannelLabel = (channel: string): string => {
  const labels: Record<string, string> = {
    sms: 'SMS',
  };
  return labels[channel] || 'Unknown Channel';
};

export const getChannelIcon = (channel: string): string => {
  const icons: Record<string, string> = {
    sms: '📱',
  };
  return icons[channel] || '❓';
};

// Confidence score utilities
export const getConfidenceLevel = (score: number | null): 'high' | 'medium' | 'low' | 'unknown' => {
  if (score === null || score === undefined) return 'unknown';
  if (score >= 0.8) return 'high';
  if (score >= 0.5) return 'medium';
  return 'low';
};

export const getConfidenceColor = (score: number | null): string => {
  const level = getConfidenceLevel(score);
  switch (level) {
    case 'high': return 'text-green-600 bg-green-50';
    case 'medium': return 'text-yellow-600 bg-yellow-50';
    case 'low': return 'text-red-600 bg-red-50';
    default: return 'text-gray-600 bg-gray-50';
  }
};

// Status utilities
export const getStatusColor = (status: string): string => {
  const colors: Record<string, string> = {
    pending: 'status-pending',
    confirmed: 'status-confirmed',
    cancelled: 'status-cancelled',
    completed: 'status-confirmed',
    no_show: 'status-cancelled',
  };
  return colors[status] || 'status-pending';
};

// Text utilities
export const truncateText = (text: string, maxLength: number = 100): string => {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};

// Phone number utilities
export const formatPhoneNumber = (phone: string): string => {
  // Simple phone number formatting
  if (phone.startsWith('+82')) {
    // Korean format
    return phone.replace(/(\+82)(\d{3})(\d{4})(\d{4})/, '$1 $2-$3-$4');
  }
  return phone;
};

// Array utilities
export const groupBy = <T>(array: T[], key: keyof T): Record<string, T[]> => {
  return array.reduce((groups, item) => {
    const group = String(item[key]);
    if (!groups[group]) {
      groups[group] = [];
    }
    groups[group].push(item);
    return groups;
  }, {} as Record<string, T[]>);
};

// Validation utilities
export const isValidPhoneNumber = (phone: string): boolean => {
  const phoneRegex = /^[+]?[\d\s-()]{10,}$/;
  return phoneRegex.test(phone);
};

export const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

// Local storage utilities
export const storage = {
  get: <T>(key: string): T | null => {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : null;
    } catch {
      return null;
    }
  },
  set: <T>(key: string, value: T): void => {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch {
      // Handle storage errors
    }
  },
  remove: (key: string): void => {
    localStorage.removeItem(key);
  },
};