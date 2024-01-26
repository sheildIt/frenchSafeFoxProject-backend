from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import EmailDocument, EmailElement, SentEmail, UseScenario, News
from .serializers import EmailDocumentSerializer, EmailElementSerializer, SentEmailSerializer, UseScenarioSerializer
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
import pytz
from company.models import Company
from .tasks import schedule_email_task
from datetime import datetime, timedelta
from .extractor import PromptAnalyzer
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseBadRequest

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


"""UseScenario views"""


@api_view(['GET'])
def get_all_use_scenarios(request, id):
    scenarios = UseScenario.objects.filter(company=id)
    serializer = UseScenarioSerializer(scenarios, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_use_scenario(request, scenario_id):
    scenario = UseScenario.objects.get(id=scenario_id)
    serializer = UseScenarioSerializer(scenario)
    return Response(serializer.data)


@api_view(['POST'])
def create_use_scenario(request):
    print(request.data)
    serializer = UseScenarioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def update_use_scenario(request, scenario_id):
    scenario = UseScenario.objects.get(id=scenario_id)
    serializer = UseScenarioSerializer(instance=scenario, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def delete_use_scenario(request, scenario_id):
    scenario = UseScenario.objects.get(id=scenario_id)
    scenario.delete()
    return Response({"message": "Scenario deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def create_ai_scenario(request):

    data = request.data
    company = Company.objects.get(id=data['company'])
    news_object = News.objects.get(id=data['news_id'])
    prompt_analyzer = PromptAnalyzer()
    keywords = prompt_analyzer.extract_keywords(news_object.article_text)

    scenario_text = (
        f"Write an email acting as a representative from {company.company_name} department {data['poi']}"
        f"Based on the latest news - {news_object.headline}, and its content: '{news_object.article_text}' "
        f"here are keywords {': '.join(keywords)}. "
        f"where employees can "
        f"participate by clicking a {data['link']}."
    )

    scenario = UseScenario.objects.create(scenario=scenario_text,
                                          title=news_object.headline,
                                          company=company,
                                          name=data['name'],
                                          poi_email=data['poi_email'],
                                          POI=data['poi'],
                                          link_field=data['link'],
                                          )

    return Response('Created!', status=status.HTTP_200_OK)


@api_view(['GET'])
def keywords_analysis(request, id):

    all_prompts = UseScenario.objects.filter(company__id=id)

    prompts_objects = [prompts.scenario for prompts in all_prompts]
    prompt_analyzer = PromptAnalyzer()

    common_keywords = prompt_analyzer.keyword_counter(prompts_objects)

    return Response('Most common keywords:', common_keywords)


def track_link(request, tracking_code):
    # Find the EmailDocument associated with the tracking_code
    email_document = get_object_or_404(
        EmailDocument, tracking_link=tracking_code)

    # Update the click count in the EmailDocument
    email_document.email_sents += 1
    email_document.save()

    # Redirect the user to the destination specified in the EmailDocument
    # Replace with the actual field storing the destination
    destination = email_document.link_field
    return redirect(destination)
