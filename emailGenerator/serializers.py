from rest_framework import serializers
from .models import EmailDocument, EmailElement, SentEmail


class EmailDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailDocument
        fields = '__all__'


class EmailElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailElement
        fields = '__all__'


class SentEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentEmail
        fields = '__all__'
