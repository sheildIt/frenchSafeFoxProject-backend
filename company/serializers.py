from .models import Company, Departments, Employee, Progress, DepartmentProgress
from rest_framework.serializers import ModelSerializer


class CompanySerializer(ModelSerializer):

    class Meta:
        model = Company
        fields = ['id', 'company_name', 'departments_list']


class DepartmentsSerializer(ModelSerializer):
    class Meta:
        model = Departments
        fields = '__all__'


class EmployeeSerializer(ModelSerializer):
    department = DepartmentsSerializer()

    class Meta:
        model = Employee
        fields = '__all__'


class ProgressSerializer(ModelSerializer):
    employee = EmployeeSerializer()

    class Meta:
        model = Progress
        fields = '__all__'


class DepartmentsProgressSerializer(ModelSerializer):
    department = DepartmentsSerializer()

    class Meta:
        model = DepartmentProgress
        fields = '__all__'
