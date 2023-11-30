from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone


class Mailbox(models.Model):
    host = models.CharField(blank=False, help_text="SMTP server address")
    port = models.IntegerField(default=465, blank=False, help_text="Connection port")
    login = models.CharField(blank=False)
    password = models.CharField(blank=False)
    email_from = models.CharField(
        blank=False, help_text="Sender name visible in the email"
    )
    use_ssl = models.BooleanField(default=True, blank=False, help_text="Use of SSL")
    is_active = models.BooleanField(default=False, help_text="Inbox activity")
    date = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(
        default=timezone.now,
        help_text="The value automatically changed upon mailbox update",
    )

    @property
    def sent(self):
        # return Email.objects.filter(mailbox=self)
        return len(self.emails)


class Template(models.Model):
    subject = models.CharField(blank=False, help_text="Subject of the message")
    text = models.TextField(blank=False, help_text="Message content")
    attachment = models.FileField(
        blank=True, null=True, help_text="Attachment to the message"
    )
    date = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(
        default=timezone.now,
        help_text="The value automatically changed upon template update",
    )


class Email(models.Model):
    mailbox = models.ForeignKey(
        Mailbox, blank=False, on_delete=models.CASCADE, related_name="emails"
    )
    template = models.ForeignKey(Template, blank=False, on_delete=models.CASCADE)
    to = ArrayField(models.EmailField(), blank=False, help_text="Recipient")
    cc = ArrayField(
        models.EmailField(), blank=False, help_text="Recipients of message copies"
    )
    bcc = ArrayField(
        models.EmailField(),
        blank=False,
        help_text="Recipients of blind carbon copy of the message",
    )
    replay_to = models.EmailField(
        default=None,
        blank=False,
        help_text="Reply-to address for the message recipient",
    )
    sent_date = models.DateTimeField(
        default=None,
        help_text="Date sent - a field filled in after sending the message",
    )
    date = models.DateTimeField(default=timezone.now)
    send_attempts = models.PositiveIntegerField(default=0)
