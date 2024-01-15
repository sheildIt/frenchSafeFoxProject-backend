from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import EmailDocument, SentEmail


class SendEmailTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Assuming you have a user with id=1, replace it accordingly
        self.sender = get_user_model().objects.get(id=1)
        self.email_document = EmailDocument.objects.create(
            # your email document fields here
        )

    def test_send_email(self):
        url = reverse('send_email', args=[self.email_document.id])
        data = {
            'subject': 'Test Subject',
            'message': 'Test Message',
            'recipient_list': ['recipient1@example.com', 'recipient2@example.com'],
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(EmailDocument.objects.get(
            id=self.email_document.id).is_live)
        self.assertEqual(SentEmail.objects.count(), 1)
        sent_email = SentEmail.objects.first()
        self.assertEqual(sent_email.sender_id, self.sender)
        self.assertEqual(sent_email.email_document, self.email_document)
        self.assertEqual(sent_email.nr_of_copies, len(data['recipient_list']))

    def test_send_email_invalid_data(self):
        url = reverse('send_email', args=[self.email_document.id])
        # Send request with missing subject
        data = {
            'message': 'Test Message',
            'recipient_list': ['recipient1@example.com', 'recipient2@example.com'],
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(EmailDocument.objects.get(
            id=self.email_document.id).is_live)
        self.assertEqual(SentEmail.objects.count(), 0)
