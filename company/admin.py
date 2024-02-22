from django.contrib import admin
from .models import Company, Departments, Employee, Progress, DepartmentProgress


admin.site.register(Company)
admin.site.register(Departments)
admin.site.register(Employee)
admin.site.register(Progress)
admin.site.register(DepartmentProgress)
