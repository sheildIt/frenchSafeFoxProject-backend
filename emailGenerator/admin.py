from django.contrib import admin
from .models import EmailElement, EmailDocument, SentEmail, UseScenario, News


admin.site.register(EmailDocument)
admin.site.register(EmailElement)
admin.site.register(SentEmail)
admin.site.register(UseScenario)
admin.site.register(News)
