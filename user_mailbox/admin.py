from django.contrib import admin

from .models import Email, Mailbox, Template

admin.site.register(Mailbox)
admin.site.register(Template)
admin.site.register(Email)
