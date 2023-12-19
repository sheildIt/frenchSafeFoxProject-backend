from .models import Company, UseScenario, Departments, Employee
from rest_framework.serializers import ModelSerializer


class CompanySerializer(ModelSerializer):

    class Meta:
        model = Company
        fields = ['id', 'company_name', 'departments_list']


class UseScenarioSerializer(ModelSerializer):
    class Meta:
        model = UseScenario
        fields = ['id', 'title', 'scenario',
                  'POI', 'poi_email', 'name', 'created_at', 'company']


class DepartmentsSerializer(ModelSerializer):
    class Meta:
        model = Departments
        fields = '__all__'


class EmployeeSerializer(ModelSerializer):
    department = DepartmentsSerializer()

    class Meta:
        model = Employee
        fields = '__all__'
