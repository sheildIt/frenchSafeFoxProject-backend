from .models import Departments, Company
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=Company)
def create_departments_for_company(sender, instance, created, **kwargs):
    if created and instance.departments_list:
        department_names = [name.strip()
                            for name in instance.departments_list.split(',')]

        for department_name in department_names:
            Departments.objects.create(
                company=instance, department_name=department_name)
