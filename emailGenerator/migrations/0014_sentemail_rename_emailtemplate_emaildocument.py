# Generated by Django 4.2.7 on 2024-01-15 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0010_departments_number_of_employees'),
        ('emailGenerator', '0013_alter_emailtemplate_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='SentEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RenameModel(
            old_name='EmailTemplate',
            new_name='EmailDocument',
        ),
    ]