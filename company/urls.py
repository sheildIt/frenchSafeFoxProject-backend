# urls.py

from django.urls import path, re_path
from . import views
from .views import EmployeeListView

urlpatterns = [
    path('get/', views.get_companies, name='register_company'),
    path('get/<str:id>', views.company_view, name='register_company'),
    path('register', views.register_company, name='register_company'),

    # Departments
    path('get_departments/<str:id>', views.get_departments),

    # Employees
    re_path(r'^employees_list/(?P<id>\d+)/$',
            EmployeeListView.as_view()),
    path('api/employees/<str:company_id>/<str:employee_id>/',
         views.employee_detail),
]
