import { apiClient } from './apiClient';
import { 
  Patient, 
  Message, 
  Appointment, 
  StaffResponse, 
  SystemMetrics,
  SystemMetricsSummary,
  ApiResponse 
} from '../types';

export class PatientService {
  static async getAll(): Promise<Patient[]> {
    return apiClient.get<Patient[]>('/patients/');
  }

  static async getById(id: number): Promise<Patient> {
    return apiClient.get<Patient>(`/patients/${id}/`);
  }

  static async create(data: Partial<Patient>): Promise<Patient> {
    return apiClient.post<Patient>('/patients/', data);
  }

  static async update(id: number, data: Partial<Patient>): Promise<Patient> {
    return apiClient.put<Patient>(`/patients/${id}/`, data);
  }

  static async delete(id: number): Promise<void> {
    return apiClient.delete(`/patients/${id}/`);
  }
}

export class MessageService {
  static async getAll(params?: { patient_id?: number }): Promise<Message[]> {
    return apiClient.get<Message[]>('/messages/', params);
  }

  static async getById(id: number): Promise<Message> {
    return apiClient.get<Message>(`/messages/${id}/`);
  }

  static async create(data: Partial<Message>): Promise<Message> {
    return apiClient.post<Message>('/messages/', data);
  }

  static async update(id: number, data: Partial<Message>): Promise<Message> {
    return apiClient.put<Message>(`/messages/${id}/`, data);
  }

  static async delete(id: number): Promise<void> {
    return apiClient.delete(`/messages/${id}/`);
  }

  static async getByPatient(patientId: number): Promise<Message[]> {
    return apiClient.get<Message[]>('/messages/', { patient_id: patientId });
  }
}

export class AppointmentService {
  static async getAll(): Promise<Appointment[]> {
    return apiClient.get<Appointment[]>('/appointments/');
  }

  static async getById(id: number): Promise<Appointment> {
    return apiClient.get<Appointment>(`/appointments/${id}/`);
  }

  static async create(data: Partial<Appointment>): Promise<Appointment> {
    return apiClient.post<Appointment>('/appointments/', data);
  }

  static async update(id: number, data: Partial<Appointment>): Promise<Appointment> {
    return apiClient.put<Appointment>(`/appointments/${id}/`, data);
  }

  static async delete(id: number): Promise<void> {
    return apiClient.delete(`/appointments/${id}/`);
  }
}

export class StaffResponseService {
  static async getAll(): Promise<StaffResponse[]> {
    return apiClient.get<StaffResponse[]>('/staff-responses/');
  }

  static async getById(id: number): Promise<StaffResponse> {
    return apiClient.get<StaffResponse>(`/staff-responses/${id}/`);
  }

  static async create(data: Partial<StaffResponse>): Promise<StaffResponse> {
    return apiClient.post<StaffResponse>('/staff-responses/', data);
  }

  static async update(id: number, data: Partial<StaffResponse>): Promise<StaffResponse> {
    return apiClient.put<StaffResponse>(`/staff-responses/${id}/`, data);
  }

  static async delete(id: number): Promise<void> {
    return apiClient.delete(`/staff-responses/${id}/`);
  }
}

export class SystemMetricsService {
  static async getAll(): Promise<SystemMetrics[]> {
    return apiClient.get<SystemMetrics[]>('/system-metrics/');
  }

  static async getById(id: number): Promise<SystemMetrics> {
    return apiClient.get<SystemMetrics>(`/system-metrics/${id}/`);
  }

  static async getSummary(): Promise<SystemMetricsSummary> {
    return apiClient.get<SystemMetricsSummary>('/system-metrics/summary/');
  }
}

export class MessageProcessorService {
  static async processMessage(data: {
    channel: string;
    recipient: string;
    content: string;
    timestamp?: string;
  }): Promise<any> {
    return apiClient.post('/process-message/', data);
  }
}

export class HealthService {
  static async check(): Promise<{
    status: string;
    timestamp: string;
    services: Record<string, string>;
  }> {
    return apiClient.get('/health/');
  }
}