from django.db import models
from company.models import Company, Departments
import uuid
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


class UseScenario(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    created_at = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=255)
    scenario = models.TextField(
        help_text='Write a scenario where an email will be sent..')
    POI = models.CharField(max_length=255, help_text='Person of Interest')
    poi_email = models.EmailField()
    link_field = models.URLField(default=None, blank=True, null=True)

    def __str__(self):
        return self.title


class EmailElement(models.Model):
    email_subjectline = models.CharField(max_length=50)
    email_text = models.TextField()
    image = models.ImageField(null=True, blank=True)
    button = models.CharField(max_length=50, null=True, blank=True)


class EmailDocument(models.Model):
    TEMPLATE_TYPE_CHOICES = [
        ('Type1', 'Standard Email'),
        ('Type2', 'Phishing Email'),
        # Add more template types as needed
    ]
    EMAIL_TYPE_CHOICES = [
        ("PROMOTIONAL", 'Promotional'),
        ("COLD", 'Cold'),
        ("OTHER", 'Other'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    template_type = models.CharField(
        max_length=50, choices=TEMPLATE_TYPE_CHOICES)
    email_type = models.CharField(
        max_length=25, choices=EMAIL_TYPE_CHOICES)
    email_theme = models.CharField(max_length=40)
    email_elements = models.ManyToManyField('EmailElement')
    friendly_url = models.CharField(max_length=150, blank=True, null=True)
    tracking_link = models.URLField(default=None, blank=True, null=True)
    scenario = models.ForeignKey(
        UseScenario, on_delete=models.SET_NULL, null=True)
    scheduled = models.BooleanField(default=False)
    is_live = models.BooleanField(default=False)
    email_sents = models.IntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)

    def generate_tracking_url(self, actual_url):
        tracking_url = reverse('track_click', kwargs={'email_id': urlsafe_base64_encode(
            force_bytes(self.id)), 'url': urlsafe_base64_encode(force_bytes(actual_url))})

        print('TRACKING URL', tracking_url)
        return f"http://localhost:8000{tracking_url}"

    def __str__(self):
        return f"{self.created_at}"


class Results(models.Model):
    sender_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    email_document = models.ForeignKey(EmailDocument, on_delete=models.CASCADE)
    department = models.ForeignKey(
        Departments, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    theme = models.CharField(max_length=45)
    nr_of_copies = models.IntegerField(default=0)
    body_clicks = models.IntegerField(default=0)
    link_clicks = models.IntegerField(default=0)
    image_clicks = models.IntegerField(default=0)
    CTA_clicks = models.IntegerField(default=0)
    reported = models.IntegerField(default=0)

    def record_link_click(self):
        print('clicked recorded?')
        self.link_clicks += 1
        self.save()


class News(models.Model):

    headline = models.CharField(max_length=40)
    article_text = models.TextField()
