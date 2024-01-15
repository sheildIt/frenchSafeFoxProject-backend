from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import EmailDocument, EmailElement, SentEmail
from .serializers import EmailDocumentSerializer, EmailElementSerializer, SentEmailSerializer
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
import pytz
from .tasks import schedule_email_task
from datetime import datetime, timedelta

"""Document views"""


@api_view(['GET', 'POST'])
def email_template_list(request, id):
    if request.method == 'GET':
        is_live = request.GET.get('is_live', None)
        if is_live is not None:
            templates = EmailDocument.objects.filter(
                company=id, is_live=is_live)
        else:
            templates = EmailDocument.objects.filter(company=id)
        serializer = EmailDocumentSerializer(templates, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EmailDocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def email_template_detail(request, pk):
    try:
        template = EmailDocument.objects.get(pk=pk)
    except EmailDocument.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EmailDocumentSerializer(template)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EmailDocumentSerializer(template, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        template.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""Email Elements views"""


@api_view(['GET', 'POST'])
def email_element_list(request):
    if request.method == 'GET':
        elements = EmailElement.objects.all()
        serializer = EmailElementSerializer(elements, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EmailElementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def email_element_detail(request, pk):
    try:
        element = EmailElement.objects.get(pk=pk)
    except EmailElement.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EmailElementSerializer(element)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EmailElementSerializer(element, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        element.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""Sent Email views"""


@api_view(['GET'])
def get_sent_emails(request):
    sender_id = request.query_params.get('sender_id', None)

    if sender_id is None:
        return Response({'error': 'Sender ID is required'}, status=400)

    sent_emails = SentEmail.objects.filter(sender_id=sender_id)
    # Use your SentEmail serializer
    serializer = SentEmailSerializer(sent_emails, many=True)

    return Response(serializer.data)


@api_view(['POST'])
def send_email(request, id):

    email_obj = EmailDocument.objects.get(id=id)
    recipient_list = request.data['recipient_list']
    try:
        send_mail(
            subject=request.data['subject'],
            message=request.data['message'],
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

        return Response('Emails sent!')
    except Exception as e:

        return Response(f"Error sending email: {str(e)}")


@api_view(['POST'])
def schedule_email(request, id):
    try:
        email_obj = EmailDocument.objects.get(id=id)
        email_info = request.data
        print(email_obj.id)
        scheduled_time = datetime.fromisoformat(
            str(request.data['scheduled_time']))
        scheduled_time_utc = pytz.timezone(
            'UTC').localize(scheduled_time)
        # Adjust for the time zone difference (1 hours ahead)
        scheduled_time_local = scheduled_time_utc - timedelta(hours=1)
        current_datetime = datetime.fromisoformat(
            str(datetime.now()))
        schedule_email_task.apply_async(
            (str(email_obj.id), email_info,), eta=scheduled_time_local)

        return Response('Sending is scheduled!')
    except Exception as e:

        return Response(f"Error sending email: {str(e)}")
