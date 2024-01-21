from rest_framework import serializers
from .models import EmailDocument, EmailElement, SentEmail, UseScenario, News


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


class UseScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = UseScenario
        fields = ['id', 'title', 'scenario',
                  'POI', 'poi_email', 'name', 'created_at', 'company', 'link_field']


class NewsSerlizier(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
