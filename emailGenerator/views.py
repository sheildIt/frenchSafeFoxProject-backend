from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import EmailDocument, EmailElement, Results, UseScenario, News
from .serializers import EmailDocumentSerializer, EmailElementSerializer, SentEmailSerializer, UseScenarioSerializer
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
import pytz
from company.models import Company, Progress
from .tasks import schedule_email_task
from datetime import datetime, timedelta
from .extractor import PromptAnalyzer
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseBadRequest, Http404
from django.shortcuts import redirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

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
def email_template_detail(request, id):
    try:
        template = EmailDocument.objects.get(id=id)
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
def email_element_list(request, id):
    if request.method == 'GET':
        email_document = EmailDocument.objects.get(id=id)

        serializer = EmailElementSerializer(
            email_document.email_elements, many=True)

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
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = EmailElementSerializer(
            element, data=request.data, partial=True)
        print(request.data)
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

    sent_emails = Results.objects.filter(sender_id=sender_id)
    # Use your SentEmail serializer
    serializer = SentEmailSerializer(sent_emails, many=True)

    return Response(serializer.data)


@api_view(['POST'])
def send_email(request, id):

    email_obj = EmailDocument.objects.get(id=id)
    recipient_list = request.data['recipient_list']
    # tracking_url = email_obj.generate_tracking_url(email_obj.friendly_url)

    for recipient_email in recipient_list:
        tracking_url = email_obj.generate_tracking_url(
            email_obj.friendly_url, recipient_email)
        email_body = request.data['message'].replace(
            email_obj.friendly_url, tracking_url)

    email_body = request.data['message'].replace(
        email_obj.friendly_url, tracking_url)
    try:
        send_mail(
            subject=request.data['subject'],
            message=email_body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=recipient_list,
            fail_silently=False,
        )

        try:
            with transaction.atomic():
                sent_email = Results.objects.create(
                    sender_id=email_obj.company,
                    email_document=email_obj,
                    theme=email_obj.email_theme,
                    nr_of_copies=len(recipient_list),
                )
                email_obj.is_live = True
                email_obj.save()
        except Exception as e:
            return Response(f"Error during database operations: {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response('Emails sent!')
    except Exception as e:

        return Response(f"Error sending email: {str(e)}")


@api_view(['POST'])
def schedule_email(request, id):
    try:
        email_obj = EmailDocument.objects.get(id=id)
        email_info = request.data

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


def track_click(request, email_id, url, recipient_email):
    try:
        email_id = force_str(urlsafe_base64_decode(email_id))
        url = force_str(urlsafe_base64_decode(url))

        email_document = EmailDocument.objects.get(id=email_id)
        result = Results.objects.get(email_document=email_document)
        recipient_email = force_str(urlsafe_base64_decode(recipient_email))
        # Record link click
        print(recipient_email)
        result.record_link_click()
        if recipient_email:
            employee_progress = Progress.objects.get(
                employee__email_address=recipient_email)
            employee_progress.link_clicks += 1
            employee_progress.save()
        # Redirect user to the actual target URL
        return redirect(f'https://www.{url}')
    except (EmailDocument.DoesNotExist, Results.DoesNotExist):
        raise Http404("Invalid tracking link")


"""API for outlook plugin"""


def email_report(request, title):
    email_document = get_object_or_404(
        EmailDocument, email_elements__subject_line=title)

    result = Results.objects.get(email_document=email_document.id)

    result.reported += 1
    result.save()

    return Response('Email reported')
