# Generated by Django 4.2.7 on 2024-01-20 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailGenerator', '0021_emaildocument_tracking_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='emaildocument',
            name='friendly_url',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]