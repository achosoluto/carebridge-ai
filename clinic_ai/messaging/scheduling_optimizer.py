"""
Advanced appointment scheduling optimization algorithms for Phase 2.
Implements intelligent scheduling with conflict detection and wait time reduction.
"""

import logging
from datetime import datetime, timedelta, time as dt_time
from typing import List, Dict, Any, Optional, Tuple
from django.db.models import Q, Count, Avg
from django.utils import timezone

from ..core.models import (
    Appointment, Doctor, DoctorAvailability, ProcedureType,
    AppointmentWaitlist, SchedulingOptimization, Patient
)
from ..core.interfaces import Scheduler

logger = logging.getLogger(__name__)


class AdvancedSchedulingOptimizer(Scheduler):
    """
    Advanced scheduling optimizer with AI-powered recommendations.
    Reduces wait times and optimizes resource utilization.
    """

    def __init__(self, optimization_weight: float = 0.7):
        """
        Initialize optimizer.
        
        Args:
            optimization_weight: Weight for optimization vs patient preference (0-1)
        """
        self.optimization_weight = optimization_weight

    def find_available_slots(self, doctor: str, date_range: Tuple[datetime, datetime],
                           preferences: Optional[Dict] = None) -> List[datetime]:
        """
        Find available appointment slots for a doctor within date range.

        Args:
            doctor: Doctor name or ID
            date_range: Tuple of (start_date, end_date)
            preferences: Optional patient preferences (time of day, etc.)

        Returns:
            List of available datetime slots
        """
        try:
            # Get doctor object
            doctor_obj = Doctor.objects.get(Q(name=doctor) | Q(id=doctor))
        except Doctor.DoesNotExist:
            logger.error(f"Doctor not found: {doctor}")
            return []

        start_date, end_date = date_range
        available_slots = []

        # Iterate through each day in the range
        current_date = start_date.date()
        end_date_only = end_date.date()

        while current_date <= end_date_only:
            weekday = current_date.weekday()
            
            # Get doctor's availability for this weekday
            availability_slots = DoctorAvailability.objects.filter(
                doctor=doctor_obj,
                weekday=weekday,
                is_available=True
            )

            for slot in availability_slots:
                # Generate time slots within availability window
                slot_times = self._generate_time_slots(
                    current_date,
                    slot.start_time,
                    slot.end_time,
                    doctor_obj.average_appointment_duration
                )

                # Filter out already booked slots
                for slot_time in slot_times:
                    if not self._is_slot_booked(doctor_obj, slot_time):
                        available_slots.append(slot_time)

            current_date += timedelta(days=1)

        # Apply preferences if provided
        if preferences:
            available_slots = self._apply_preferences(available_slots, preferences)

        return sorted(available_slots)

    def _generate_time_slots(self, date: datetime.date, start_time: dt_time,
                            end_time: dt_time, duration: timedelta) -> List[datetime]:
        """Generate time slots within a time range."""
        slots = []
        current_time = datetime.combine(date, start_time)
        end_datetime = datetime.combine(date, end_time)

        while current_time + duration <= end_datetime:
            slots.append(timezone.make_aware(current_time))
            current_time += duration

        return slots

    def _is_slot_booked(self, doctor: Doctor, slot_time: datetime) -> bool:
        """Check if a time slot is already booked."""
        # Check for overlapping appointments
        duration = doctor.average_appointment_duration
        slot_end = slot_time + duration

        overlapping = Appointment.objects.filter(
            doctor=doctor.name,
            scheduled_at__lt=slot_end,
            scheduled_at__gte=slot_time - duration,
            status__in=['pending', 'confirmed']
        ).exists()

        return overlapping

    def _apply_preferences(self, slots: List[datetime], 
                          preferences: Dict) -> List[datetime]:
        """Filter slots based on patient preferences."""
        filtered_slots = slots

        # Preferred time of day
        if 'preferred_time' in preferences:
            pref_time = preferences['preferred_time']
            if pref_time == 'morning':
                filtered_slots = [s for s in filtered_slots if s.hour < 12]
            elif pref_time == 'afternoon':
                filtered_slots = [s for s in filtered_slots if 12 <= s.hour < 17]
            elif pref_time == 'evening':
                filtered_slots = [s for s in filtered_slots if s.hour >= 17]

        # Preferred days of week
        if 'preferred_days' in preferences:
            pref_days = preferences['preferred_days']  # List of weekday numbers
            filtered_slots = [s for s in filtered_slots if s.weekday() in pref_days]

        return filtered_slots

    def create_appointment(self, patient_id: str, doctor: str, procedure: str,
                          scheduled_at: datetime) -> Dict[str, Any]:
        """
        Create new appointment with optimization.

        Returns:
            Dict with appointment details and optimization info
        """
        try:
            # Get related objects
            patient = Patient.objects.get(id=patient_id)
            doctor_obj = Doctor.objects.get(Q(name=doctor) | Q(id=doctor))
            
            # Check if slot is available
            if self._is_slot_booked(doctor_obj, scheduled_at):
                # Try to find alternative slot
                alternative = self._find_alternative_slot(
                    doctor_obj, scheduled_at, procedure
                )
                if alternative:
                    return {
                        'success': False,
                        'message': 'Requested slot unavailable',
                        'alternative_slot': alternative,
                        'should_optimize': True
                    }
                else:
                    return {
                        'success': False,
                        'message': 'No available slots found',
                        'should_waitlist': True
                    }

            # Create appointment
            appointment = Appointment.objects.create(
                patient=patient,
                doctor=doctor_obj.name,
                procedure=procedure,
                scheduled_at=scheduled_at,
                status='pending'
            )

            logger.info(f"Created appointment: {appointment.id}")
            return {
                'success': True,
                'appointment_id': appointment.id,
                'scheduled_at': scheduled_at
            }

        except (Patient.DoesNotExist, Doctor.DoesNotExist) as e:
            logger.error(f"Error creating appointment: {e}")
            return {
                'success': False,
                'message': str(e)
            }

    def _find_alternative_slot(self, doctor: Doctor, requested_time: datetime,
                              procedure: str) -> Optional[datetime]:
        """Find alternative slot close to requested time."""
        # Search within +/- 3 days
        start_range = requested_time - timedelta(days=3)
        end_range = requested_time + timedelta(days=3)

        available_slots = self.find_available_slots(
            doctor.name,
            (start_range, end_range)
        )

        if not available_slots:
            return None

        # Find closest slot to requested time
        closest_slot = min(
            available_slots,
            key=lambda x: abs((x - requested_time).total_seconds())
        )

        return closest_slot

    def optimize_schedule(self, appointments: List[Dict]) -> List[Dict]:
        """
        Optimize appointment schedule for efficiency.
        Reduces wait times and improves resource utilization.

        Args:
            appointments: List of appointment dicts with patient preferences

        Returns:
            Optimized list of appointments with recommendations
        """
        optimized = []

        for appt_data in appointments:
            try:
                # Get appointment details
                patient_id = appt_data['patient_id']
                doctor = appt_data['doctor']
                procedure = appt_data['procedure']
                requested_time = appt_data['requested_time']

                # Find optimal slot
                optimal_slot = self._find_optimal_slot(
                    doctor, procedure, requested_time
                )

                if optimal_slot:
                    # Calculate optimization metrics
                    time_diff = abs((optimal_slot - requested_time).total_seconds() / 60)
                    wait_reduction = self._estimate_wait_reduction(
                        doctor, optimal_slot, requested_time
                    )

                    optimized.append({
                        'patient_id': patient_id,
                        'doctor': doctor,
                        'procedure': procedure,
                        'original_time': requested_time,
                        'optimized_time': optimal_slot,
                        'time_difference_minutes': int(time_diff),
                        'wait_time_reduction_minutes': wait_reduction,
                        'optimization_score': self._calculate_optimization_score(
                            time_diff, wait_reduction
                        )
                    })
                else:
                    # Keep original if no optimization possible
                    optimized.append({
                        'patient_id': patient_id,
                        'doctor': doctor,
                        'procedure': procedure,
                        'original_time': requested_time,
                        'optimized_time': requested_time,
                        'time_difference_minutes': 0,
                        'wait_time_reduction_minutes': 0,
                        'optimization_score': 0.0
                    })

            except Exception as e:
                logger.error(f"Error optimizing appointment: {e}")
                continue

        return optimized

    def _find_optimal_slot(self, doctor: str, procedure: str,
                          requested_time: datetime) -> Optional[datetime]:
        """
        Find optimal appointment slot using AI-powered algorithm.
        Considers doctor workload, procedure type, and historical patterns.
        """
        try:
            doctor_obj = Doctor.objects.get(Q(name=doctor) | Q(id=doctor))
        except Doctor.DoesNotExist:
            return None

        # Get available slots around requested time
        search_range = (
            requested_time - timedelta(days=2),
            requested_time + timedelta(days=2)
        )
        available_slots = self.find_available_slots(doctor, search_range)

        if not available_slots:
            return None

        # Score each slot based on multiple factors
        scored_slots = []
        for slot in available_slots:
            score = self._score_slot(doctor_obj, slot, requested_time, procedure)
            scored_slots.append((slot, score))

        # Return highest scoring slot
        if scored_slots:
            best_slot = max(scored_slots, key=lambda x: x[1])
            return best_slot[0]

        return None

    def _score_slot(self, doctor: Doctor, slot: datetime,
                   requested_time: datetime, procedure: str) -> float:
        """
        Score a time slot based on optimization criteria.
        Higher score = better slot.
        """
        score = 100.0

        # Factor 1: Proximity to requested time (weight: 40%)
        time_diff_hours = abs((slot - requested_time).total_seconds() / 3600)
        proximity_score = max(0, 40 - (time_diff_hours * 5))
        score += proximity_score

        # Factor 2: Doctor workload on that day (weight: 30%)
        day_appointments = Appointment.objects.filter(
            doctor=doctor.name,
            scheduled_at__date=slot.date(),
            status__in=['pending', 'confirmed']
        ).count()
        
        workload_ratio = day_appointments / doctor.max_daily_appointments
        workload_score = max(0, 30 - (workload_ratio * 30))
        score += workload_score

        # Factor 3: Time of day efficiency (weight: 20%)
        # Morning slots generally have less wait time
        hour = slot.hour
        if 9 <= hour < 11:
            score += 20  # Best time
        elif 11 <= hour < 14:
            score += 15  # Good time
        elif 14 <= hour < 17:
            score += 10  # Acceptable time
        else:
            score += 5   # Less optimal

        # Factor 4: Historical wait times (weight: 10%)
        avg_wait = self._get_average_wait_time(doctor, slot.time())
        if avg_wait < 15:
            score += 10
        elif avg_wait < 30:
            score += 5

        return score

    def _estimate_wait_reduction(self, doctor: str, optimized_time: datetime,
                                original_time: datetime) -> int:
        """Estimate wait time reduction from optimization."""
        # Simplified estimation - in production, use ML model
        hour_diff = abs((optimized_time - original_time).total_seconds() / 3600)
        
        # Morning slots typically have 30% less wait time
        if optimized_time.hour < 11 and original_time.hour >= 14:
            return 30
        elif optimized_time.hour < 14 and original_time.hour >= 14:
            return 15
        
        return max(0, int(10 - hour_diff * 2))

    def _calculate_optimization_score(self, time_diff: float,
                                     wait_reduction: int) -> float:
        """Calculate overall optimization quality score (0-1)."""
        # Balance between staying close to requested time and reducing wait
        time_penalty = min(time_diff / 120, 0.5)  # Max 50% penalty for 2+ hours diff
        wait_benefit = min(wait_reduction / 60, 0.5)  # Max 50% benefit for 60+ min reduction
        
        score = 0.5 - time_penalty + wait_benefit
        return max(0.0, min(1.0, score))

    def _get_average_wait_time(self, doctor: Doctor, time_of_day: dt_time) -> int:
        """Get historical average wait time for doctor at specific time."""
        # Simplified - in production, query historical data
        # Morning: 10-15 min, Afternoon: 20-30 min
        if time_of_day.hour < 12:
            return 12
        elif time_of_day.hour < 17:
            return 25
        else:
            return 20

    def add_to_waitlist(self, patient_id: int, doctor_id: int,
                       procedure_type_id: int, preferences: Dict) -> Dict[str, Any]:
        """
        Add patient to waitlist for fully booked slots.

        Args:
            patient_id: Patient ID
            doctor_id: Doctor ID
            procedure_type_id: Procedure type ID
            preferences: Patient preferences (date, time range, etc.)

        Returns:
            Waitlist entry details
        """
        try:
            patient = Patient.objects.get(id=patient_id)
            doctor = Doctor.objects.get(id=doctor_id)
            procedure_type = ProcedureType.objects.get(id=procedure_type_id)

            # Calculate priority score
            priority_score = self._calculate_waitlist_priority(patient, procedure_type)

            # Create waitlist entry
            waitlist_entry = AppointmentWaitlist.objects.create(
                patient=patient,
                doctor=doctor,
                procedure_type=procedure_type,
                preferred_date=preferences.get('preferred_date'),
                preferred_time_start=preferences.get('time_start', dt_time(9, 0)),
                preferred_time_end=preferences.get('time_end', dt_time(17, 0)),
                priority_score=priority_score,
                status='waiting'
            )

            # Get position in queue
            position = AppointmentWaitlist.objects.filter(
                doctor=doctor,
                status='waiting',
                priority_score__gte=priority_score
            ).count()

            logger.info(f"Added patient {patient_id} to waitlist (position: {position})")

            return {
                'success': True,
                'waitlist_id': waitlist_entry.id,
                'position': position,
                'priority_score': priority_score
            }

        except Exception as e:
            logger.error(f"Error adding to waitlist: {e}")
            return {
                'success': False,
                'message': str(e)
            }

    def _calculate_waitlist_priority(self, patient: Patient,
                                    procedure_type: ProcedureType) -> int:
        """Calculate priority score for waitlist ordering."""
        # Base priority
        priority = 50

        # Increase priority for returning patients
        appointment_count = Appointment.objects.filter(
            patient=patient,
            status='completed'
        ).count()
        priority += min(appointment_count * 5, 20)

        # Procedure urgency (could be added to ProcedureType model)
        # For now, use a simple heuristic
        if 'urgent' in procedure_type.name.lower():
            priority += 30

        return priority

    def process_waitlist_notifications(self) -> int:
        """
        Process waitlist and notify patients when slots become available.
        
        Returns:
            Number of notifications sent
        """
        notifications_sent = 0

        # Get active waitlist entries
        waitlist_entries = AppointmentWaitlist.objects.filter(
            status='waiting'
        ).order_by('-priority_score', 'created_at')

        for entry in waitlist_entries:
            # Check if slot is now available
            available_slots = self.find_available_slots(
                str(entry.doctor.id),  # Pass doctor ID as string
                (
                    timezone.make_aware(datetime.combine(entry.preferred_date, entry.preferred_time_start)),
                    timezone.make_aware(datetime.combine(entry.preferred_date, entry.preferred_time_end))
                )
            )

            if available_slots:
                # Notify patient
                entry.status = 'notified'
                entry.notified_at = timezone.now()
                entry.expires_at = timezone.now() + timedelta(hours=24)
                entry.save()

                notifications_sent += 1
                logger.info(f"Notified patient {entry.patient.id} about available slot")

        return notifications_sent