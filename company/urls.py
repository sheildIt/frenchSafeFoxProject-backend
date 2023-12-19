# urls.py

from django.urls import path, re_path
from . import views
from .views import EmployeeListView

urlpatterns = [
    path('get/', views.get_companies, name='register_company'),
    path('get/<str:id>', views.company_view, name='register_company'),
    path('register', views.register_company, name='register_company'),

    # Scenarios
    path('get_scenarios/<str:id>', views.get_all_use_scenarios),
    path('get_scenario/<str:id>', views.get_use_scenario),
    path('create_scenario', views.create_use_scenario),
    path('get_scenario/<str:id>', views.update_use_scenario),
    path('delete_scenario/<str:id>', views.delete_use_scenario),

    # Departments
    path('get_departments/<str:id>', views.get_departments),

    # Employees
    re_path(r'^employees_list/(?P<id>\d+)/$',
            EmployeeListView.as_view()),
    path('api/employees/<str:id>/<str:employee_id>/',
         views.employee_detail),
]
