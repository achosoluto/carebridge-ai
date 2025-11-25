"""
Notification service for appointment reminders and staff alerts.
Supports SMS only for MVP.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from ..core.models import (
    Appointment, AppointmentReminder, Patient, Message
)
from ..core.interfaces import NotificationService

logger = logging.getLogger(__name__)


class SMSNotificationService(NotificationService):
    """
    SMS-only notification service for patient and staff communications.
    Simplified for MVP focusing on core functionality.
    """

    def __init__(self):
        self.default_channel = 'sms'
        self.reminder_templates = self._load_reminder_templates()

    def _load_reminder_templates(self) -> Dict[str, Dict[str, str]]:
        """Load notification templates for Korean and English only."""
        return {
            'appointment_reminder': {
                'ko': """
안녕하세요 {patient_name}님,

예약 알림입니다:
- 의사: {doctor}
- 시술: {procedure}
- 일시: {scheduled_at}

문의사항이 있으시면 연락주세요.
감사합니다.
                """.strip(),
                'en': """
Hello {patient_name},

Appointment Reminder:
- Doctor: {doctor}
- Procedure: {procedure}
- Date/Time: {scheduled_at}

Please contact us if you have any questions.
Thank you.
                """.strip()
            },
            'appointment_confirmation': {
                'ko': """
{patient_name}님의 예약이 확정되었습니다.

예약 정보:
- 의사: {doctor}
- 시술: {procedure}
- 일시: {scheduled_at}
- 예약번호: {appointment_id}

예약 변경이 필요하시면 연락주세요.
                """.strip(),
                'en': """
Your appointment has been confirmed, {patient_name}.

Appointment Details:
- Doctor: {doctor}
- Procedure: {procedure}
- Date/Time: {scheduled_at}
- Confirmation #: {appointment_id}

Please contact us if you need to reschedule.
                """.strip()
            },
            'waitlist_notification': {
                'ko': """
{patient_name}님,

대기 중이신 예약 시간이 가능해졌습니다!

- 의사: {doctor}
- 시술: {procedure}
- 가능 시간: {available_time}

24시간 이내에 예약을 확정해주세요.
                """.strip(),
                'en': """
{patient_name},

A slot has become available for your waitlisted appointment!

- Doctor: {doctor}
- Procedure: {procedure}
- Available Time: {available_time}

Please confirm within 24 hours.
                """.strip()
            }
        }

    def send_reminder(self, appointment_id: str, patient_contact: str, 
                     message: str) -> bool:
        """
        Send appointment reminder to patient.

        Args:
            appointment_id: Appointment ID
            patient_contact: Patient contact (phone/email)
            message: Reminder message content

        Returns:
            True if sent successfully
        """
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            patient = appointment.patient

            # Determine best channel based on patient preferences
            channel = self._determine_best_channel(patient)

            # Create reminder record
            reminder = AppointmentReminder.objects.create(
                appointment=appointment,
                scheduled_send_at=timezone.now(),
                channel=channel,
                message_content=message,
                status='pending'
            )

            # Send via appropriate channel
            success = self._send_via_channel(
                channel=channel,
                recipient=patient_contact,
                message=message,
                patient=patient
            )

            # Update reminder status
            if success:
                reminder.status = 'sent'
                reminder.sent_at = timezone.now()
            else:
                reminder.status = 'failed'
                reminder.error_message = 'Failed to send notification'
            
            reminder.save()

            logger.info(f"Reminder sent for appointment {appointment_id} via {channel}")
            return success

        except Appointment.DoesNotExist:
            logger.error(f"Appointment not found: {appointment_id}")
            return False
        except Exception as e:
            logger.error(f"Error sending reminder: {e}")
            return False

    def _determine_best_channel(self, patient: Patient) -> str:
        """For MVP, always return SMS as the only supported channel."""
        return 'sms'

    def _send_via_channel(self, channel: str, recipient: str,
                         message: str, patient: Patient) -> bool:
        """Send notification via SMS channel only (MVP)."""
        try:
            if channel == 'sms':
                return self._send_sms(recipient, message)
            else:
                logger.warning(f"Only SMS channel supported in MVP: {channel}")
                return False
        except Exception as e:
            logger.error(f"Error sending via {channel}: {e}")
            return False

    def _send_sms(self, recipient: str, message: str) -> bool:
        """Send SMS notification (placeholder for SMS service integration)."""
        # In production, integrate with SMS service (Twilio, AWS SNS, etc.)
        logger.info(f"SMS would be sent to {recipient}: {message[:50]}...")
        return True

    def notify_staff(self, message: str, priority: str = 'normal') -> bool:
        """
        Notify staff about system events or patient needs.

        Args:
            message: Notification message
            priority: Priority level (low, normal, high, urgent)

        Returns:
            True if sent successfully
        """
        try:
            staff_email = settings.CLINIC_AI.get('STAFF_NOTIFICATION_EMAIL')
            
            if not staff_email:
                logger.warning("Staff notification email not configured")
                return False

            subject = f"[{priority.upper()}] CareBridge AI Staff Alert"
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[staff_email],
                fail_silently=False
            )

            logger.info(f"Staff notification sent: {priority}")
            return True

        except Exception as e:
            logger.error(f"Error sending staff notification: {e}")
            return False

    def send_appointment_confirmation(self, appointment_id: int) -> bool:
        """Send appointment confirmation to patient."""
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            patient = appointment.patient

            # Get template in patient's language
            template = self.reminder_templates['appointment_confirmation'].get(
                patient.preferred_language, 
                self.reminder_templates['appointment_confirmation']['en']
            )

            # Format message
            message = template.format(
                patient_name=patient.name or 'Patient',
                doctor=appointment.doctor,
                procedure=appointment.procedure,
                scheduled_at=appointment.scheduled_at.strftime('%Y-%m-%d %H:%M'),
                appointment_id=appointment.id
            )

            # Send notification
            return self.send_reminder(
                appointment_id=str(appointment.id),
                patient_contact=patient.phone,
                message=message
            )

        except Appointment.DoesNotExist:
            logger.error(f"Appointment not found: {appointment_id}")
            return False

    def send_waitlist_notification(self, waitlist_id: int, 
                                   available_time: datetime) -> bool:
        """Notify patient about available waitlist slot."""
        try:
            from ..core.models import AppointmentWaitlist
            
            waitlist = AppointmentWaitlist.objects.get(id=waitlist_id)
            patient = waitlist.patient

            # Get template in patient's language
            template = self.reminder_templates['waitlist_notification'].get(
                patient.preferred_language,
                self.reminder_templates['waitlist_notification']['en']
            )

            # Format message
            message = template.format(
                patient_name=patient.name or 'Patient',
                doctor=waitlist.doctor.name,
                procedure=waitlist.procedure_type.name,
                available_time=available_time.strftime('%Y-%m-%d %H:%M')
            )

            # Determine channel and send
            channel = self._determine_best_channel(patient)
            success = self._send_via_channel(
                channel=channel,
                recipient=patient.phone,
                message=message,
                patient=patient
            )

            if success:
                waitlist.status = 'notified'
                waitlist.notified_at = timezone.now()
                waitlist.save()

            return success

        except Exception as e:
            logger.error(f"Error sending waitlist notification: {e}")
            return False

    def schedule_reminder(self, appointment_id: int, 
                         hours_before: int = 24) -> bool:
        """
        Schedule an appointment reminder to be sent.

        Args:
            appointment_id: Appointment ID
            hours_before: Hours before appointment to send reminder

        Returns:
            True if scheduled successfully
        """
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            patient = appointment.patient

            # Calculate send time
            send_time = appointment.scheduled_at - timedelta(hours=hours_before)

            # Don't schedule if appointment is too soon
            if send_time <= timezone.now():
                logger.warning(f"Appointment {appointment_id} too soon for reminder")
                return False

            # Get template
            template = self.reminder_templates['appointment_reminder'].get(
                patient.preferred_language,
                self.reminder_templates['appointment_reminder']['en']
            )

            # Format message
            message = template.format(
                patient_name=patient.name or 'Patient',
                doctor=appointment.doctor,
                procedure=appointment.procedure,
                scheduled_at=appointment.scheduled_at.strftime('%Y-%m-%d %H:%M')
            )

            # Create scheduled reminder
            channel = self._determine_best_channel(patient)
            reminder = AppointmentReminder.objects.create(
                appointment=appointment,
                scheduled_send_at=send_time,
                channel=channel,
                message_content=message,
                status='pending'
            )

            logger.info(f"Scheduled reminder for appointment {appointment_id} at {send_time}")
            return True

        except Appointment.DoesNotExist:
            logger.error(f"Appointment not found: {appointment_id}")
            return False
        except Exception as e:
            logger.error(f"Error scheduling reminder: {e}")
            return False

    def process_pending_reminders(self) -> int:
        """
        Process and send all pending reminders that are due.
        Should be called by a scheduled task (Celery).

        Returns:
            Number of reminders sent
        """
        sent_count = 0

        # Get pending reminders that are due
        pending_reminders = AppointmentReminder.objects.filter(
            status='pending',
            scheduled_send_at__lte=timezone.now()
        )

        for reminder in pending_reminders:
            try:
                appointment = reminder.appointment
                patient = appointment.patient

                # Send reminder
                success = self._send_via_channel(
                    channel=reminder.channel,
                    recipient=patient.phone,
                    message=reminder.message_content,
                    patient=patient
                )

                # Update status
                if success:
                    reminder.status = 'sent'
                    reminder.sent_at = timezone.now()
                    sent_count += 1
                else:
                    reminder.status = 'failed'
                    reminder.error_message = 'Failed to send'
                
                reminder.save()

            except Exception as e:
                logger.error(f"Error processing reminder {reminder.id}: {e}")
                reminder.status = 'failed'
                reminder.error_message = str(e)
                reminder.save()

        logger.info(f"Processed {sent_count} pending reminders")
        return sent_count