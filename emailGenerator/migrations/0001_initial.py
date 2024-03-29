# Generated by Django 4.2.7 on 2024-02-13 09:52

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailDocument',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('template_type', models.CharField(choices=[('Type1', 'Standard Email'), ('Type2', 'Phishing Email')], max_length=50)),
                ('email_type', models.CharField(choices=[('PROMOTIONAL', 'Promotional'), ('COLD', 'Cold'), ('OTHER', 'Other')], max_length=25)),
                ('email_theme', models.CharField(max_length=40)),
                ('friendly_url', models.CharField(blank=True, max_length=150, null=True)),
                ('tracking_link', models.URLField(blank=True, default=None, null=True)),
                ('scheduled', models.BooleanField(default=False)),
                ('is_live', models.BooleanField(default=False)),
                ('email_sents', models.IntegerField(default=0)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company')),
            ],
        ),
        migrations.CreateModel(
            name='EmailElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_subjectline', models.CharField(max_length=50)),
                ('email_text', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('button', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=40)),
                ('article_text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='UseScenario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('title', models.CharField(max_length=255)),
                ('scenario', models.TextField(help_text='Write a scenario where an email will be sent..')),
                ('POI', models.CharField(help_text='Person of Interest', max_length=255)),
                ('poi_email', models.EmailField(max_length=254)),
                ('link_field', models.URLField(blank=True, default=None, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company')),
            ],
        ),
        migrations.CreateModel(
            name='SentEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('theme', models.CharField(max_length=45)),
                ('nr_of_copies', models.IntegerField(default=0)),
                ('body_clicks', models.IntegerField(default=0)),
                ('link_clicks', models.IntegerField(default=0)),
                ('image_clicks', models.IntegerField(default=0)),
                ('CTA_clicks', models.IntegerField(default=0)),
                ('reported', models.IntegerField(default=0)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company.departments')),
                ('email_document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emailGenerator.emaildocument')),
                ('sender_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company')),
            ],
        ),
        migrations.AddField(
            model_name='emaildocument',
            name='email_elements',
            field=models.ManyToManyField(to='emailGenerator.emailelement'),
        ),
        migrations.AddField(
            model_name='emaildocument',
            name='scenario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='emailGenerator.usescenario'),
        ),
    ]
