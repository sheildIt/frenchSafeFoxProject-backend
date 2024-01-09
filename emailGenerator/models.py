from django.db import models
from company.models import Company, UseScenario
import uuid


class EmailTemplate(models.Model):
    TEMPLATE_TYPE_CHOICES = [
        ('Type1', 'Standard Email'),
        ('Type2', 'Phishing Email'),
        # Add more template types as needed
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    template_type = models.CharField(
        max_length=50, choices=TEMPLATE_TYPE_CHOICES)
    email_subjectline = models.CharField(max_length=50)
    email_body = models.TextField()
    scenario = models.ForeignKey(
        UseScenario, on_delete=models.SET_NULL, null=True)
    scheduled = models.BooleanField(default=False)
    is_live = models.BooleanField(default=False)
    email_sents = models.IntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):

        return f"{self.email_subjectline} - {self.created_at}"


class EmailElement(models.Model):
    ELEMENT_TYPE_CHOICES = [
        ('TypeA', 'Type A'),
        ('TypeB', 'Type B'),
        # Add more element types as needed
    ]

    email_template = models.ForeignKey(EmailTemplate, on_delete=models.CASCADE)
    element_type = models.CharField(
        max_length=50, choices=ELEMENT_TYPE_CHOICES)
    email_text = models.TextField()
    image = models.ImageField(upload_to='email_images/', null=True, blank=True)
    button = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.element_type} - {self.email_template}"
