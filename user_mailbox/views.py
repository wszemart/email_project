import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Email, Mailbox, Template
from .serializers import EmailSerializer, MailboxSerializer, TemplateSerializer
from .tasks import send_email_task

logger = logging.getLogger(__name__)


class MailboxViewSet(viewsets.ModelViewSet):
    queryset = Mailbox.objects.all()
    serializer_class = MailboxSerializer


class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer


class EmailViewSet(viewsets.ModelViewSet):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["sent_date", "date"]

    @action(detail=False, methods=["post"])
    def send_email(self, request):
        try:
            mailbox_id = request.data.get("mailbox_id")
            template_id = request.data.get("template_id")

            mailbox = Mailbox.objects.get(pk=mailbox_id)
            template = Template.objects.get(pk=template_id)

            if not mailbox.is_active:
                logger.error("Mailbox is not active.")
                return Response(
                    {"error": "Mailbox is not active."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            email = Email.objects.create(mailbox=mailbox, template=template)
            send_email_task.delay(email.id)

            logger.info(f"Email sent successfully. Email ID: {email.id}")

            return Response(
                {"success": "Email sent successfully. Check logs for details."},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.exception(f"An error {e} occurred while sending email.")
            return Response(
                {"error": "An error occurred while sending email."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
