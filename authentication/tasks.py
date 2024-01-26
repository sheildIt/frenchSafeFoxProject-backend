# views.py
from celery import shared_task
from django.utils import timezone
from .models import AuthCode
import uuid


@shared_task
def review_auth_code(auth_code_id: uuid):
    try:
        auth_code_obj = AuthCode.objects.get(id=auth_code_id)
        auth_code_obj.expired = True
        auth_code_obj.save()
    except AuthCode.DoesNotExist:
        return f'AuthCode with ID {auth_code_id} does not exist'
    except Exception as e:
        return f'There has been an error: {str(e)}'
