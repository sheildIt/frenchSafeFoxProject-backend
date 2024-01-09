from django.urls import path
from . import views

urlpatterns = [
    path('email_templates/<str:id>/', views.email_template_list,
         name='email_template_list'),
    path('email_templates/<int:pk>/', views.email_template_detail,
         name='email_template_detail'),
    path('email_elements/', views.email_element_list, name='email_element_list'),
    path('email_elements/<int:pk>/', views.email_element_detail,
         name='email_element_detail'),
    path('send_email/<str:id>', views.send_email)

]
