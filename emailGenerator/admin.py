from django.contrib import admin
from .models import EmailElement, EmailDocument, Results, UseScenario, News


admin.site.register(EmailDocument)
admin.site.register(EmailElement)
admin.site.register(Results)
admin.site.register(UseScenario)
admin.site.register(News)
