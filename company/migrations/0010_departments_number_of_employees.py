# Generated by Django 4.2.7 on 2024-01-09 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0009_alter_employee_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='departments',
            name='number_of_employees',
            field=models.IntegerField(default=0),
        ),
    ]