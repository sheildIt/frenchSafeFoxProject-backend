from django.contrib import admin
from .models import EmailElement, EmailDocument, SentEmail


admin.site.register(EmailDocument)
admin.site.register(EmailElement)
admin.site.register(SentEmail)
