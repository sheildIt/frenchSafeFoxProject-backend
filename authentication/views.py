from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import AuthCode
from django.core.mail import send_mail
from django.contrib.auth.models import User
import uuid
from django.conf import settings
from .tasks import review_auth_code


@api_view(['POST'])
def generate_auth_code(request):
    # Assuming you pass the user's email in the request data
    user_email = request.data.get('user_email')

    # Check if the user exists
    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Generate AuthCode
    auth_code = AuthCode.objects.create(user=user, code=uuid.uuid4())
    print(auth_code.expiration_time)
    if auth_code.expired is False:
        review_auth_code.apply_async(
            (auth_code.id,), eta=auth_code.expiration_time)

    # Send email with the auth code
    subject = 'SheildIT - Authentication Code'
    message = f'Your authentication code is: {auth_code.code}\n\nPlease use this code to authenticate and be aware that it will expire in 5 mins!.'

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)

    return Response({'message': 'Authentication code sent successfully.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def validate_auth_code(request):
    try:
        # Get the authentication code from the request data
        auth_code = request.data.get('auth_code')

        # Check if the code exists and is not expired or used
        auth_code_obj = AuthCode.objects.get(
            code=auth_code, expired=False, is_used=False)

        # Mark the code as used
        auth_code_obj.is_used = True
        auth_code_obj.save()

        return Response({'message': 'Authentication successful.'}, status=status.HTTP_200_OK)

    except AuthCode.DoesNotExist:
        return Response({'error': 'Invalid authentication code.'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': f'There has been an error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
