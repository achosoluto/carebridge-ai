"""
Notification service for appointment reminders and staff alerts.
Supports multiple channels: SMS, Email, KakaoTalk, WeChat, LINE.
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


class MultiChannelNotificationService(NotificationService):
    """
    Multi-channel notification service for patient and staff communications.
    Supports SMS, Email, and messaging platforms.
    """

    def __init__(self):
        self.default_channel = 'email'
        self.reminder_templates = self._load_reminder_templates()

    def _load_reminder_templates(self) -> Dict[str, Dict[str, str]]:
        """Load notification templates for different languages."""
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
                """.strip(),
                'zh': """
您好 {patient_name}，

预约提醒：
- 医生：{doctor}
- 手术：{procedure}
- 日期/时间：{scheduled_at}

如有疑问请联系我们。
谢谢。
                """.strip(),
                'ja': """
{patient_name}様

予約のお知らせ：
- 医師：{doctor}
- 施術：{procedure}
- 日時：{scheduled_at}

ご質問がございましたらご連絡ください。
ありがとうございます。
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
                """.strip(),
                'zh': """
{patient_name}，您的预约已确认。

预约详情：
- 医生：{doctor}
- 手术：{procedure}
- 日期/时间：{scheduled_at}
- 确认号：{appointment_id}

如需更改预约请联系我们。
                """.strip(),
                'ja': """
{patient_name}様、ご予約が確定しました。

予約詳細：
- 医師：{doctor}
- 施術：{procedure}
- 日時：{scheduled_at}
- 確認番号：{appointment_id}

予約変更が必要な場合はご連絡ください。
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
                """.strip(),
                'zh': """
{patient_name}，

您等待的预约时间现已可用！

- 医生：{doctor}
- 手术：{procedure}
- 可用时间：{available_time}

请在24小时内确认预约。
                """.strip(),
                'ja': """
{patient_name}様、

お待ちいただいていた予約枠が空きました！

- 医師：{doctor}
- 施術：{procedure}
- 利用可能時間：{available_time}

24時間以内にご確認ください。
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
        """Determine best notification channel for patient."""
        # Check recent message history to see preferred channel
        recent_messages = Message.objects.filter(
            patient=patient
        ).order_by('-created_at')[:5]

        if recent_messages:
            # Use most recent channel
            return recent_messages[0].channel
        
        # Default to email
        return 'email'

    def _send_via_channel(self, channel: str, recipient: str, 
                         message: str, patient: Patient) -> bool:
        """Send notification via specific channel."""
        try:
            if channel == 'email':
                return self._send_email(recipient, message, patient)
            elif channel == 'sms':
                return self._send_sms(recipient, message)
            elif channel == 'kakao':
                return self._send_kakao(recipient, message)
            elif channel == 'wechat':
                return self._send_wechat(recipient, message)
            elif channel == 'line':
                return self._send_line(recipient, message)
            else:
                logger.warning(f"Unsupported channel: {channel}")
                return False
        except Exception as e:
            logger.error(f"Error sending via {channel}: {e}")
            return False

    def _send_email(self, recipient: str, message: str, patient: Patient) -> bool:
        """Send email notification."""
        try:
            subject = "Appointment Reminder - CareBridge AI"
            from_email = settings.CLINIC_AI.get('STAFF_NOTIFICATION_EMAIL', 'noreply@carebridge.ai')
            
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=[recipient],
                fail_silently=False
            )
            return True
        except Exception as e:
            logger.error(f"Email send error: {e}")
            return False

    def _send_sms(self, recipient: str, message: str) -> bool:
        """Send SMS notification (placeholder for SMS service integration)."""
        # In production, integrate with SMS service (Twilio, AWS SNS, etc.)
        logger.info(f"SMS would be sent to {recipient}: {message[:50]}...")
        return True

    def _send_kakao(self, recipient: str, message: str) -> bool:
        """Send KakaoTalk notification (placeholder)."""
        # In production, integrate with KakaoTalk API
        logger.info(f"KakaoTalk would be sent to {recipient}: {message[:50]}...")
        return True

    def _send_wechat(self, recipient: str, message: str) -> bool:
        """Send WeChat notification (placeholder)."""
        # In production, integrate with WeChat API
        logger.info(f"WeChat would be sent to {recipient}: {message[:50]}...")
        return True

    def _send_line(self, recipient: str, message: str) -> bool:
        """Send LINE notification (placeholder)."""
        # In production, integrate with LINE API
        logger.info(f"LINE would be sent to {recipient}: {message[:50]}...")
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