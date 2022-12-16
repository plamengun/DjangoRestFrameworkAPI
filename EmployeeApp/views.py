from django.http import JsonResponse
from django.http import Http404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.permissions import IsAuthenticated

from EmployeeApp.serializers import CompanySerializer, EmployeeSerializer
from EmployeeApp.models import Companies, Employees


def api_home(request, *args, **kwargs):
    return JsonResponse({"message": 'Hi there, this is a Django API response serving as a homepage :D'})


class CompaniesList(APIView):
    def get(self, request):
        companies = Companies.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)


class CompanyCreate(APIView):

    permission_classes = [IsAuthenticated]

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

    def get(self, request, pk):
        company = self.get_company_by_id_or_404(pk)
        serializer = CompanySerializer(company)
        return Response(serializer.data)

    def put(self, request, pk):
        company = self.get_company_by_id_or_404(pk)
        serializer = CompanySerializer(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        company = self.get_company_by_id_or_404(pk)
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmployeeCreate(APIView):

    permission_classes = [IsAuthenticated]

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


    def get(self, request, pk):
        employee = self.get_employee_by_id_or_404(pk)
        company = self.check_if_logged_as_company(request)
        if self.check_if_employee_part_of_company(employee, company):
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)

    def put(self, request, pk):
        employee = self.get_employee_by_id_or_404(pk)
        company = self.check_if_logged_as_company(request)
        if self.check_if_employee_part_of_company(employee, company):
            serializer = EmployeeSerializer(employee, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        employee = self.get_employee_by_id_or_404(pk)
        company = self.check_if_logged_as_company(request)
        if self.check_if_employee_part_of_company(employee, company):
            employee.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)