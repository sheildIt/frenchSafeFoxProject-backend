from .models import Departments, Company, Employee
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


@receiver(post_save, sender=Company)
def create_departments_for_company(sender, instance, created, **kwargs):
    if created and instance.departments_list:
        department_names = [name.strip()
                            for name in instance.departments_list.split(',')]

        for department_name in department_names:
            Departments.objects.create(
                company=instance, department_name=department_name)


@receiver(post_delete, sender=Employee)
@receiver(post_save, sender=Employee)
def update_department_employee_count(sender, instance, **kwargs):
    # Update number_of_employees field of the associated department
    instance.department.number_of_employees = Employee.objects.filter(
        department=instance.department).count()
    instance.department.save()


# Connect the signal to the update_department_employee_count function
post_save.connect(update_department_employee_count, sender=Employee)
post_delete.connect(update_department_employee_count, sender=Employee)
