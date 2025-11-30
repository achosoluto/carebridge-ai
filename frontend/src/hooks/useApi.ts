import { useState, useEffect, useCallback } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import {
  PatientService,
  MessageService,
  AppointmentService,
  SystemMetricsService,
  MessageProcessorService
} from '../services/apiServices';
import {
  DoctorService,
  ProcedureTypeService,
  MedicalTermsService,
  SchedulingService,
  WaitlistService,
  RemindersService
} from '../services/apiServices';
import { Patient, Message, Appointment } from '../types';

// Patient hooks
export const usePatients = () => {
  return useQuery('patients', PatientService.getAll);
};

export const usePatient = (id: number) => {
  return useQuery(['patient', id], () => PatientService.getById(id), {
    enabled: !!id,
  });
};

export const useCreatePatient = () => {
  const queryClient = useQueryClient();
  return useMutation(PatientService.create, {
    onSuccess: () => {
      queryClient.invalidateQueries('patients');
    },
  });
};

export const useUpdatePatient = () => {
  const queryClient = useQueryClient();
  return useMutation(
    ({ id, data }: { id: number; data: Partial<Patient> }) =>
      PatientService.update(id, data),
    {
      onSuccess: (_, variables) => {
        queryClient.invalidateQueries('patients');
        queryClient.invalidateQueries(['patient', variables.id]);
      },
    }
  );
};

export const useDeletePatient = () => {
  const queryClient = useQueryClient();
  return useMutation(PatientService.delete, {
    onSuccess: () => {
      queryClient.invalidateQueries('patients');
    },
  });
};

// Message hooks
export const useMessages = (patientId?: number) => {
  return useQuery(['messages', { patientId }], () =>
    MessageService.getAll(patientId ? { patient_id: patientId } : undefined)
  );
};

export const useMessage = (id: number) => {
  return useQuery(['message', id], () => MessageService.getById(id), {
    enabled: !!id,
  });
};

export const useMessagesByPatient = (patientId: number) => {
  return useQuery(['messages', 'patient', patientId],
    () => MessageService.getByPatient(patientId),
    { enabled: !!patientId }
  );
};

export const useCreateMessage = () => {
  const queryClient = useQueryClient();
  return useMutation(MessageService.create, {
    onSuccess: () => {
      queryClient.invalidateQueries('messages');
    },
  });
};

export const useUpdateMessage = () => {
  const queryClient = useQueryClient();
  return useMutation(
    ({ id, data }: { id: number; data: Partial<Message> }) =>
      MessageService.update(id, data),
    {
      onSuccess: (_, variables) => {
        queryClient.invalidateQueries('messages');
        queryClient.invalidateQueries(['message', variables.id]);
      },
    }
  );
};

// Appointment hooks
export const useAppointments = () => {
  return useQuery('appointments', AppointmentService.getAll);
};

export const useAppointment = (id: number) => {
  return useQuery(['appointment', id], () => AppointmentService.getById(id), {
    enabled: !!id,
  });
};

export const useCreateAppointment = () => {
  const queryClient = useQueryClient();
  return useMutation(AppointmentService.create, {
    onSuccess: () => {
      queryClient.invalidateQueries('appointments');
    },
  });
};

export const useUpdateAppointment = () => {
  const queryClient = useQueryClient();
  return useMutation(
    ({ id, data }: { id: number; data: Partial<Appointment> }) =>
      AppointmentService.update(id, data),
    {
      onSuccess: (_, variables) => {
        queryClient.invalidateQueries('appointments');
        queryClient.invalidateQueries(['appointment', variables.id]);
      },
    }
  );
};

export const useDeleteAppointment = () => {
  const queryClient = useQueryClient();
  return useMutation(AppointmentService.delete, {
    onSuccess: () => {
      queryClient.invalidateQueries('appointments');
    },
  });
};

// System metrics hooks
export const useSystemMetrics = () => {
  return useQuery('systemMetrics', SystemMetricsService.getAll);
};

export const useSystemMetricsSummary = () => {
  return useQuery('systemMetricsSummary', SystemMetricsService.getSummary);
};

// Message processor hook
export const useMessageProcessor = () => {
  return useMutation(MessageProcessorService.processMessage);
};

// Real-time updates hook
export const useRealTimeUpdates = (intervalMs: number = 30000) => {
  const [isConnected, setIsConnected] = useState(true);

  const { data: messages } = useQuery('messages', () => MessageService.getAll(), {
    refetchInterval: intervalMs,
    refetchOnWindowFocus: true,
  });

  const { data: appointments } = useQuery('appointments', AppointmentService.getAll, {
    refetchInterval: intervalMs * 2, // Less frequent updates for appointments
    refetchOnWindowFocus: true,
  });

  const { data: systemMetrics } = useQuery('systemMetricsSummary', SystemMetricsService.getSummary, {
    refetchInterval: intervalMs * 3, // Even less frequent for metrics
    refetchOnWindowFocus: true,
  });

  useEffect(() => {
    const handleOnline = () => setIsConnected(true);
    const handleOffline = () => setIsConnected(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return {
    isConnected,
    messages: messages || [],
    appointments: appointments || [],
    systemMetrics,
  };
};

// WebSocket-like polling hook for live message updates
export const useLiveMessages = (patientId?: number) => {
  const queryClient = useQueryClient();
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  const { data: messages, isLoading, error } = useQuery(
    ['live-messages', patientId],
    () => MessageService.getAll(patientId ? { patient_id: patientId } : undefined),
    {
      refetchInterval: 5000, // Poll every 5 seconds for real-time feel
      refetchIntervalInBackground: true,
    }
  );

  const updateLastUpdate = useCallback(() => {
    setLastUpdate(new Date());
  }, []);

  useEffect(() => {
    if (messages) {
      updateLastUpdate();
    }
  }, [messages, updateLastUpdate]);

  return {
    messages: messages || [],
    isLoading,
    error,
    lastUpdate,
    refresh: () => {
      queryClient.invalidateQueries(['live-messages', patientId]);
    },
  };
};


// Phase 2 Hooks

// Lists
export const useDoctors = () => {
  return useQuery('doctors', DoctorService.getAll);
};

export const useProcedureTypes = () => {
  return useQuery('procedureTypes', ProcedureTypeService.getAll);
};

export const useMedicalTermsCategories = () => {
  return useQuery('medicalTermsCategories', MedicalTermsService.getCategories);
};

export const useMedicalTermsSearch = (query: string) => {
  return useQuery({
    queryKey: ['medicalTermsSearch', query],
    queryFn: () => MedicalTermsService.search(query),
    enabled: !!query && query.length > 2,
  });
};

// Mutations
export const useGetAvailableSlots = () => {
  return useMutation(SchedulingService.getAvailableSlots);
};

export const useOptimizeScheduling = () => {
  const queryClient = useQueryClient();
  return useMutation(SchedulingService.optimizeScheduling, {
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['appointments'] });
    },
  });
};

export const useAddToWaitlist = () => {
  const queryClient = useQueryClient();
  return useMutation(WaitlistService.addToWaitlist, {
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['appointments'] });
    },
  });
};

export const useProcessWaitlistNotifications = () => {
  const queryClient = useQueryClient();
  return useMutation(WaitlistService.processNotifications);
};

export const useScheduleReminder = () => {
  const queryClient = useQueryClient();
  return useMutation(RemindersService.scheduleReminder, {
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['appointments'] });
    },
  });
};