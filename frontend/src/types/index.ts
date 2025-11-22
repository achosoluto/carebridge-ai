// API Types based on Django models
export interface Patient {
  id: number;
  phone: string;
  name: string;
  preferred_language: 'ko' | 'en' | 'zh' | 'ja';
  created_at: string;
  updated_at: string;
}

export interface Message {
  id: number;
  patient: number;
  patient_name: string;
  patient_phone: string;
  content: string;
  direction: 'incoming' | 'outgoing';
  channel: 'kakao' | 'wechat' | 'line' | 'sms' | 'phone';
  is_ai_handled: boolean;
  needs_human: boolean;
  confidence_score: number | null;
  created_at: string;
  updated_at: string;
}

export interface Appointment {
  id: number;
  patient: number;
  patient_name: string;
  patient_phone: string;
  doctor: string;
  procedure: string;
  scheduled_at: string;
  status: 'pending' | 'confirmed' | 'completed' | 'cancelled' | 'no_show';
  notes: string;
  approved_by: number | null;
  approved_by_name: string | null;
  created_at: string;
  updated_at: string;
}

export interface StaffResponse {
  id: number;
  message: number;
  message_preview: string;
  staff_user: number;
  staff_user_name: string;
  content: string;
  response_time: string | null;
  satisfaction_rating: number | null;
  created_at: string;
  updated_at: string;
}

export interface SystemMetrics {
  id: number;
  date: string;
  total_messages: number;
  ai_handled_messages: number;
  human_needed_messages: number;
  completed_appointments: number;
  average_response_time: string | null;
  patient_satisfaction_avg: number | null;
  created_at: string;
  updated_at: string;
}

export interface SystemMetricsSummary {
  total_messages: number;
  ai_handled: number;
  human_required: number;
  completed_appointments: number;
}

// UI State Types
export interface ChatMessage {
  id: number;
  content: string;
  direction: 'incoming' | 'outgoing';
  timestamp: string;
  channel: string;
  is_ai_handled: boolean;
  needs_human: boolean;
  confidence_score?: number | null;
}

// Form Types
export interface PatientFormData {
  phone: string;
  name: string;
  preferred_language: 'ko' | 'en' | 'zh' | 'ja';
}

export interface AppointmentFormData {
  patient_id: number;
  doctor: string;
  procedure: string;
  scheduled_at: string;
  notes?: string;
}

// Response Types
export interface ApiResponse<T> {
  results: T[];
  count: number;
  next: string | null;
  previous: string | null;
}

export interface ApiError {
  detail: string;
  code?: string;
}

// Language support
export interface Language {
  code: 'ko' | 'en' | 'zh' | 'ja';
  name: string;
  flag: string;
}

export const SUPPORTED_LANGUAGES: Language[] = [
  { code: 'ko', name: '한국어', flag: '🇰🇷' },
  { code: 'en', name: 'English', flag: '🇺🇸' },
  { code: 'zh', name: '中文', flag: '🇨🇳' },
  { code: 'ja', name: '日本語', flag: '🇯🇵' },
];

// Channel support
export const CHANNELS = [
  { value: 'kakao', label: 'KakaoTalk', icon: '💬' },
  { value: 'wechat', label: 'WeChat', icon: '💚' },
  { value: 'line', label: 'LINE', icon: '🟢' },
  { value: 'sms', label: 'SMS', icon: '📱' },
  { value: 'phone', label: 'Phone', icon: '📞' },
];
// Phase 2 API Types

export interface Doctor {
  id: number;
  name: string;
  specialization: string;
  email: string;
  phone: string;
  is_active: boolean;
  max_daily_appointments: number;
  average_appointment_duration: string;
  created_at: string;
}

export interface ProcedureType {
  id: number;
  name: string;
  name_ko: string;
  name_zh: string;
  name_ja: string;
  description: string;
  estimated_duration: string;
  requires_equipment: string;
  preparation_time: string;
  recovery_time: string;
}

export interface MedicalTerm {
  id: number;
  term_en: string;
  term_ko: string;
  term_zh: string;
  term_ja: string;
  category: string;
  description: string;
  usage_count: number;
  accuracy_rating: number;
  created_at: string;
}

export interface AvailableSlotsRequest {
  doctor_id: number;
  start_date: string;
  end_date: string;
  preferred_time?: 'morning' | 'afternoon' | 'evening' | 'any';
}

export interface AvailableSlotsResponse {
  doctor_id: number;
  doctor_name: string;
  available_slots: string[];
  total_slots: number;
}

export interface OptimizeSchedulingRequest {
  patient_id: number;
  doctor_id: number;
  procedure_type_id: number;
  requested_time: string;
  preferences?: {
    preferred_time?: 'morning' | 'afternoon' | 'evening';
  };
}

export interface SchedulingOptimization {
  patient_id: number;
  doctor: string;
  procedure: string;
  original_time: string;
  optimized_time: string;
  time_difference_minutes: number;
  wait_time_reduction_minutes: number;
  optimization_score: number;
}

export interface OptimizeSchedulingResponse {
  success: boolean;
  optimization: SchedulingOptimization;
}

export interface WaitlistAddRequest {
  patient_id: number;
  doctor_id: number;
  procedure_type_id: number;
  preferred_date: string;
  preferred_time_start: string;
  preferred_time_end: string;
}

export interface WaitlistAddResponse {
  success: boolean;
  waitlist_id: number;
  position: number;
  priority_score: number;
}

export interface WaitlistProcessResponse {
  success: boolean;
  notifications_sent: number;
}

export interface ReminderScheduleRequest {
  appointment_id: number;
  hours_before: number;
}

export interface ReminderScheduleResponse {
  success: boolean;
  appointment_id: number;
  hours_before: number;
}