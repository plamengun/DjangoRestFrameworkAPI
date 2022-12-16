from django.http import JsonResponse
from django.http import Http404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.permissions import IsAuthenticated

from EmployeeApp.serializers import CompanySerializer, EmployeeSerializer
from EmployeeApp.models import Companies, Employees

from drf_yasg.utils import swagger_auto_schema


def api_home(request, *args, **kwargs):
    return JsonResponse({"message": 'Hi there, this is a Django API response serving as a homepage :D'})


class CompaniesList(APIView):
    @swagger_auto_schema(
        operation_summary="List all companies",
        operation_description="This returns a list of all companies to any viewer"
    )
    def get(self, request):
        companies = Companies.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)


class CompanyCreate(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Create a company",
        operation_description="This allows logged-in user to create a company"
    )
    def post(self, request):
        company_name_exists = Companies.objects.filter(company_name=request.data['company_name']).exists()
        if company_name_exists:
            raise ValidationError("Company with the same name already exists")

        data = {**request.data, 'user_id': request.auth.user_id}

        serializer = CompanySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyDetails(APIView):

    permission_classes = [IsAuthenticated]

    def get_company_by_id_or_404(self, pk):
        try:
            return Companies.objects.get(pk=pk)
        except Companies.DoesNotExist:
            raise Http404()

    def check_if_company_belongs_to_user(self, request, company):
        if request.auth.user_id != company.user_id:
            raise ValidationError("Company does not belong to you")
        return True


    @swagger_auto_schema(
        operation_summary="Get a company by id",
        operation_description="This allows a logged-in user to access detailed company info"
    )
    def get(self, request, pk):
        company = self.get_company_by_id_or_404(pk)
        if self.check_if_company_belongs_to_user(request, company):
            serializer = CompanySerializer(company)
            return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Edit company info",
        operation_description="This allows a logged-in user to edit the company info"
    )
    def put(self, request, pk):
        company = self.get_company_by_id_or_404(pk)
        if self.check_if_company_belongs_to_user(request, company):
            serializer = CompanySerializer(company, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a company",
        operation_description="This allows a logged-in user to delete a company"
    )
    def delete(self, request, pk):
        company = self.get_company_by_id_or_404(pk)
        if self.check_if_company_belongs_to_user(request, company):
            company.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class EmployeeCreate(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Create an employee",
        operation_description="This allows a logged-in company to create an employee"
    )
    def post(self, request):
        company = Companies.objects.get(user_id=request.auth.user_id)
        if not company:
            raise ValidationError("You must be logged-in as a company")

        data = {**request.data, 'company_id': company.id}

        serializer = EmployeeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeesList(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="List all employees",
        operation_description="This allows a company to view a list of all it's employees"
    )
    def get(self, request):
        company = Companies.objects.get(user_id=request.auth.user_id)
        if not company:
            raise ValidationError("You must be logged-in as a company")

        employees = Employees.objects.filter(company_id=company.id)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)


class EmployeeDetails(APIView):

    permission_classes = [IsAuthenticated]
    
    def check_if_logged_as_company(self, request):
        company = Companies.objects.get(user_id=request.auth.user_id)
        if not company:
            raise ValidationError("You must be logged-in as a company")
        return company

    def get_employee_by_id_or_404(self, pk):
        try:
            return Employees.objects.get(pk=pk)
        except Employees.DoesNotExist:
            raise Http404()

    def check_if_employee_part_of_company(self, employee, company):
        if employee.company_id != company.id:
            raise ValidationError("Employee is not part of your company")
        return True

    @swagger_auto_schema(
        operation_summary="Get an employee by id",
        operation_description="This allows a logged-in company to access info for one of it's employees"
    )
    def get(self, request, pk):
        employee = self.get_employee_by_id_or_404(pk)
        company = self.check_if_logged_as_company(request)
        if self.check_if_employee_part_of_company(employee, company):
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Edit employee info",
        operation_description="This allows a company to edit the info of one of it's employees"
    )
    def put(self, request, pk):
        employee = self.get_employee_by_id_or_404(pk)
        company = self.check_if_logged_as_company(request)
        if self.check_if_employee_part_of_company(employee, company):
            serializer = EmployeeSerializer(employee, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete employee",
        operation_description="This allows a company to delete one of it's employees"
    )
    def delete(self, request, pk):
        employee = self.get_employee_by_id_or_404(pk)
        company = self.check_if_logged_as_company(request)
        if self.check_if_employee_part_of_company(employee, company):
            employee.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)