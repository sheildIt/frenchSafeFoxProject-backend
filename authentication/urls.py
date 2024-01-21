from django.urls import path
from . import views

urlpatterns = [
    # Other URLs...
    path('generate-auth-code/', views.generate_auth_code,
         name='generate_auth_code'),
    path('validate-auth-code/', views.validate_auth_code,
         name='validate_auth_code'),
]
