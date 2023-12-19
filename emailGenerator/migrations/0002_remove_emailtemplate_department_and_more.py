# Generated by Django 4.2.7 on 2023-12-11 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0009_alter_employee_date_created'),
        ('emailGenerator', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailtemplate',
            name='department',
        ),
        migrations.AddField(
            model_name='emailtemplate',
            name='department_list',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.departments'),
        ),
        migrations.AddField(
            model_name='emailtemplate',
            name='email_body',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='emailtemplate',
            name='email_subjectline',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='emailtemplate',
            name='scenario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.usescenario'),
        ),
    ]
