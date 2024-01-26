from django.shortcuts import render
from .models import Company, Departments, Employee
from .serializers import CompanySerializer, DepartmentsSerializer, EmployeeSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView


"""COMPANY VIEWS"""


@api_view(['GET'])
def get_companies(request):
    companies = Company.objects.filter().all()
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def company_view(request, id):
    company = Company.objects.get(id=id)
    serializer = CompanySerializer(company)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def register_company(request):
    if request.method == 'POST':
        serializer = CompanySerializer(data=request.data)

        if serializer.is_valid():
            # Customize this logic based on your requirements
            # Assuming you are using TokenAuthentication or another authentication method
            company = serializer.save()

            return Response({'company_id': company.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({'detail': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


"""DEPARTMENTS views"""


@api_view(['GET'])
def get_departments(request, id):
    departments = Departments.objects.filter(company=id)
    serializer = DepartmentsSerializer(departments, many=True)

    return Response({"departments": serializer.data}, status=status.HTTP_200_OK)


"""EMPLOYEE VIEWS"""


class EmployeeListView(ListAPIView):
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        company_id = self.kwargs['id']
        queryset = Employee.objects.filter(company=company_id)

        # Get a list of department IDs from the query parameters
        department_ids = self.request.GET.getlist('department')

        # Filter the queryset based on the department IDs
        if department_ids:
            queryset = queryset.filter(department__in=department_ids)

        return queryset


@api_view(['GET', 'PUT', 'DELETE'])
def employee_detail(request, company_id, employee_id):
    try:
        employee = Employee.objects.filter(
            company=company_id, id=employee_id).first()
        print(company_id, employee_id)
    except Employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Retrieve a specific employee
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Update a specific employee
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Delete a specific employee
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
