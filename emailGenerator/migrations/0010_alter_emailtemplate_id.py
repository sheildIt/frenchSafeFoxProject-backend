# Generated by Django 4.2.7 on 2024-01-09 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emailGenerator', '0009_alter_emailtemplate_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailtemplate',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]