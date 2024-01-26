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

    # Scenarios
    path('get_scenarios/<str:id>', views.get_all_use_scenarios),
    path('get_scenario/<str:id>', views.get_use_scenario),
    path('create_scenario', views.create_ai_scenario),
    path('create_scenario_manual', views.create_use_scenario),
    path('get_scenario/<str:id>', views.update_use_scenario),
    path('delete_scenario/<str:id>', views.delete_use_scenario),


    # SendEmail
    path('send_email/<str:id>', views.send_email),
    path('schedule_email/<str:id>', views.schedule_email),
    path('live_emails', views.get_sent_emails),


    # Keywords analysis
    path('keywords_analysis/<str:id>', views.keywords_analysis),

    # link tracking
    path('track-link/<str:tracking_code>/',
         views.track_link, name='track_link'),
]
