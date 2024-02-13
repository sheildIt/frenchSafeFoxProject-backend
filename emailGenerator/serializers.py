from rest_framework import serializers
from .models import EmailDocument, EmailElement, SentEmail, UseScenario, News


class EmailElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailElement
        fields = '__all__'


class EmailDocumentSerializer(serializers.ModelSerializer):
    email_elements = EmailElementSerializer(many=True)

    class Meta:
        model = EmailDocument
        fields = '__all__'

    def create(self, validated_data):
        email_elements_data = validated_data.pop('email_elements')
        email_document = EmailDocument.objects.create(**validated_data)

        for email_element_data in email_elements_data:
            email_element = EmailElement.objects.create(
                **email_element_data)
            email_document.email_elements.add(email_element)
        return email_document


class SentEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentEmail
        fields = '__all__'


class UseScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = UseScenario
        fields = ['id', 'title', 'scenario',
                  'POI', 'poi_email', 'name', 'created_at', 'company', 'link_field']


class NewsSerlizier(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
