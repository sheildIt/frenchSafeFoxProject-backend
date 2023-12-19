from django.contrib import admin
from .models import EmailElement, EmailTemplate


admin.site.register(EmailTemplate)
admin.site.register(EmailElement)
