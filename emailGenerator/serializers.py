from rest_framework import serializers
from .models import EmailTemplate, EmailElement


class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = '__all__'


class EmailElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailElement
        fields = '__all__'
