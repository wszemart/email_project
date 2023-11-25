from rest_framework.routers import DefaultRouter

from .views import EmailViewSet, MailboxViewSet, TemplateViewSet

router = DefaultRouter()
router.register(r"mailboxes", MailboxViewSet, basename="mailbox")
router.register(r"templates", TemplateViewSet, basename="template")
router.register(r"emails", EmailViewSet, basename="email")

urlpatterns = router.urls
