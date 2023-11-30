import time

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from user_mailbox.models import Email


@shared_task
def send_email_task(email_id):
    time.sleep(5)
    email = Email.objects.get(pk=email_id)

    if email.send_attempts >= 3:
        email.save()
        return

    try:
        subject = email.template.subject
        text = email.template.text
        from_email = email.mailbox.email_from
        to_emails = email.to

        send_mail(
            subject,
            text,
            from_email,
            to_emails,
            fail_silently=False,
        )

        email.sent_date = timezone.now()
        email.save()

    except Exception as e:
        email.send_attempts += 1
        email.save()
        raise e
