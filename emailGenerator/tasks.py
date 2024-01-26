from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.conf import settings
from .models import SentEmail, EmailDocument
from django.db import transaction
from django.core.mail import send_mail
import uuid


@shared_task
def schedule_email_task(email_object: uuid, email_info: dict):
    email_obj = EmailDocument.objects.get(id=email_object)
    print(
        f"Received task with email_object: {email_object}, email_info: {email_info}")
    recipient_list = email_info['recipient_list']
    print(email_info['subject'])
    try:
        send_mail(
            subject=email_info['subject'],
            message=email_info['message'],
            # Replace with your sender email
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=False,
        )

        with transaction.atomic:
            sent_email = SentEmail.objects.create(
                sender_id=email_obj.company,
                email_document=email_obj,
                # You may want to adjust this based on your requirements
                theme=email_obj.email_theme,
                nr_of_copies=len(recipient_list),
            )

            email_obj.is_live = True
            email_obj.save()

    except Exception as e:
        print("Error sending SMS:", str(e))
