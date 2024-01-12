from django.db import models
from django.contrib.auth.models import User
import random


class Company(models.Model):
    company_name = models.CharField(max_length=255, blank=False)
    departments_list = models.TextField(
        blank=True, help_text="Enter a comma-separated list of department names")
    img = models.ImageField(upload_to='company_images/', blank=True, null=True)

    def __str__(self):
        return self.company_name


class UseScenario(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    created_at = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=255)
    scenario = models.TextField(
        help_text='Write a scenario where email will be sent..')
    POI = models.CharField(max_length=255, help_text='person of interest')
    poi_email = models.EmailField()
    link_field = models.URLField(default=None, blank=True, null=True)

    def __str__(self):
        return self.title


class Departments(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    department_name = models.CharField(max_length=40)
    color_choices = ['red', 'blue', 'pink',
                     'purple', 'slate', 'green', 'yellow', 'orange', 'amber', 'emerald', 'teal']
    color = models.CharField(
        max_length=7, default='color')
    incidents = models.IntegerField(default=0)
    number_of_employees = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        def color_lambda():
            return random.choice(self.color_choices)

        chose_color = color_lambda()
        self.color = chose_color
        super().save(*args, **kwargs)

    def __str__(self):
        return self.department_name


class Employee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    email_address = models.EmailField(unique=True)
    date_created = models.DateField(auto_created=True)

    @property
    def formatted_date(self):
        return self.date_created.strftime("%Y-%m-%d")
