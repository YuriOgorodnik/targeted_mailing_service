from apscheduler.schedulers.background import BackgroundScheduler

from config.settings import EMAIL_HOST_USER
from .models import MailingMessage, MailingLog
from django.core.mail import send_mail

scheduler = BackgroundScheduler()
scheduler.start()


def send_mailing(mailing_message_pk):
    """
    Функция отправки рассылки по указанному идентификатору.
    """
    try:
        mailing_message = MailingMessage.objects.get(pk=mailing_message_pk)
        recipients = mailing_message.mailing.recipients.all()

        if mailing_message.mailing.status != 'completed':
            for recipient in recipients:
                subject = mailing_message.subject
                message_body = mailing_message.body
                from_email = EMAIL_HOST_USER
                to_email = [recipient.email]

                try:
                    # Отправка сообщения
                    send_mail(subject, message_body, from_email, to_email, fail_silently=False)

                    # Сбор статистики
                    message_log = MailingLog.objects.create(
                        message=mailing_message,
                        status='Sent'
                    )
                    message_log.save()

                except Exception as e:
                    # Обработка ошибок отправки
                    message_log = MailingLog.objects.create(
                        message=mailing_message,
                        status='Error',
                        server_response=str(e)
                    )
                    message_log.save()

            # Обновление статуса рассылки на "Завершена"
            mailing_message.mailing.status = 'completed'
            mailing_message.mailing.save()

    except MailingMessage.DoesNotExist:
        print(f"Рассылка с идентификатором {mailing_message_pk} не найдена")


def schedule_mailing(mailing_message_pk, start_date):
    """
    Функция планирования рассылки на указанную дату и время.
    """
    try:
        mailing_message = MailingMessage.objects.get(pk=mailing_message_pk)

        # Проверка статуса рассылки перед планированием
        if mailing_message.mailing.status != 'completed':
            mailing_message.mailing.status = 'started'
            mailing_message.mailing.save()

        scheduler.add_job(
            send_mailing,
            'date',
            run_date=start_date,
            args=[mailing_message_pk]
        )
    except Exception as e:
        # Обработка ошибок при планировании рассылки
        print(f"Ошибка при планировании рассылки: {e}")
