# Generated by Django 4.2.7 on 2024-02-21 18:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emailGenerator', '0003_results_employees_reported_list'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='results',
            name='department',
        ),
    ]
