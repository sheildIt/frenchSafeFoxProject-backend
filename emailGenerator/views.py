from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import EmailTemplate, EmailElement
from .serializers import EmailTemplateSerializer, EmailElementSerializer
from django.core.mail import send_mail
from django.conf import settings


# EmailTemplate views
@api_view(['GET', 'POST'])
def email_template_list(request, id):
    if request.method == 'GET':
        is_live = request.GET.get('is_live', None)
        if is_live is not None:
            templates = EmailTemplate.objects.filter(
                company=id, is_live=is_live)
        else:
            templates = EmailTemplate.objects.filter(company=id)
        serializer = EmailTemplateSerializer(templates, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EmailTemplateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def email_template_detail(request, pk):
    try:
        template = EmailTemplate.objects.get(pk=pk)
    except EmailTemplate.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EmailTemplateSerializer(template)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EmailTemplateSerializer(template, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        template.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# EmailElement views

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


@api_view(['POST'])
def send_email(request, id):

    email_obj = EmailTemplate.objects.get(id=id)

    try:
        send_mail(
            subject=request.data['subject'],
            message=request.data['message'],
            # Replace with your sender email
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=request.data['recipient_list'],
            fail_silently=False,
        )

        email_obj.is_live = True
        email_obj.save()

        return Response('Emails sent!')
    except Exception as e:

        return Response(f"Error sending email: {str(e)}")
