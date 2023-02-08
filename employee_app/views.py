from django.http import JsonResponse
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.permissions import IsAuthenticated
from employee_app.serializers import CompanySerializer, EmployeeSerializer
from employee_app.models import Companies, Employees
from drf_yasg.utils import swagger_auto_schema


def api_home(request, *args, **kwargs):
    return JsonResponse({"message": 'Hi there, this is a Django API '
                                    'response serving as a homepage :D'})


class CompaniesList(APIView):
    @swagger_auto_schema(
        operation_summary="List all companies",
        operation_description="This returns a list of all companies to any viewer",
        tags=["Company Endpoints"],
    )
    def get(self, request):

        """
        View all companies
        :param request:
        :return Response:
        """

        companies = Companies.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)


class CompanyCreate(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=CompanySerializer,
        operation_summary="Create a company",
        operation_description="This allows logged-in user to create a company",
        tags=["Company Endpoints"],
    )
    def post(self, request):

        """
        Create a company as a logged-in user
        :param request: Request Body & Auth user data
        :return Response | ValidationError:
        """

        company_name_exists =\
            Companies.objects.filter(company_name=request.data['company_name']).exists()
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

    @staticmethod
    def get_company_by_id_or_404(pk):
        try:
            return Companies.objects.get(pk=pk)
        except Companies.DoesNotExist:
            raise Http404()

    @staticmethod
    def check_if_company_belongs_to_user(request, company):
        if request.auth.user_id != company.user_id:
            raise ValidationError("Company does not belong to you")
        return True

    @swagger_auto_schema(
        operation_summary="Get a company by id",
        operation_description="This allows a logged-in user to access detailed company info",
        tags=["Company Endpoints"],
    )
    def get(self, request, pk):

        """
        Get company info by id
        :param request:
        :param pk: company_id
        :return: Company | Http404
        """

        company = self.get_company_by_id_or_404(pk)
        if self.check_if_company_belongs_to_user(request, company):
            serializer = CompanySerializer(company)
            return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CompanySerializer,
        operation_summary="Edit company info",
        operation_description="This allows a logged-in user to edit the company info",
        tags=["Company Endpoints"],
    )
    def patch(self, request, pk):

        """
        Edit company info
        :param request:
        :param pk: company_id
        :return: Company | Http400
        """

        company = self.get_company_by_id_or_404(pk)
        if self.check_if_company_belongs_to_user(request, company):
            serializer = CompanySerializer(company, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a company",
        operation_description="This allows a logged-in user to delete a company",
        tags=["Company Endpoints"],
    )
    def delete(self, request, pk):

        """
        Delete a company
        :param request:
        :param pk: company_id
        :return: Http204
        """

        company = self.get_company_by_id_or_404(pk)
        if self.check_if_company_belongs_to_user(request, company):
            company.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class EmployeeCreate(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=EmployeeSerializer,
        operation_summary="Create an employee",
        operation_description="This allows a logged-in company to create an employee",
        tags=["Employee Endpoints"],
    )
    def post(self, request, pk: int):

        """
        Creates an employee. Adds it under the logged-in company.
        :param request: Request Body & Auth user data
        :param pk: Company ID
        :return Response: Employee | ValidationError
        """

        company = Companies.objects.get(id=pk)
        if company.user_id != request.auth.user_id:
            raise ValidationError("The selected company does not belong to you.")

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
        operation_summary="List all employees for a given company",
        operation_description="This allows a company to view a list of all it's employees",
        tags=["Employee Endpoints"],
    )
    def get(self, request, pk):

        """
        List all employees of a company
        :param request:
        :param pk: company_id
        :return: List[Employee] | ValidationError
        """

        company = Companies.objects.get(id=pk)
        if company.user_id != request.auth.user_id:
            raise ValidationError("The selected company does not belong to you.")

        employees = Employees.objects.filter(company_id=company.id)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)


class EmployeeDetails(APIView):

    permission_classes = [IsAuthenticated]

    @staticmethod
    def check_if_logged_as_company(request):
        companies = Companies.objects.filter(user_id=request.auth.user_id)
        if not companies:
            raise ValidationError("You must be logged-in as a company")
        return companies

    @staticmethod
    def get_employee_by_id_or_404(pk):
        try:
            return Employees.objects.get(pk=pk)
        except Employees.DoesNotExist:
            raise Http404()

    @staticmethod
    def check_if_employee_part_of_company(employee, companies):
        for comp in companies:
            if employee.company_id == comp.id:
                return comp
        raise ValidationError("Employee is not part of your company")

    @swagger_auto_schema(
        operation_summary="Get an employee by id",
        operation_description="This allows a logged-in company "
                              "to access info for one of it's employees",
        tags=["Employee Endpoints"],
    )
    def get(self, request, pk: int):

        """
        Get employee info by id
        :param request:
        :param pk: employee_id
        :return: Employee | ValidationError
        """

        employee = self.get_employee_by_id_or_404(pk)
        companies = self.check_if_logged_as_company(request)
        if self.check_if_employee_part_of_company(employee, companies):
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)

    @swagger_auto_schema(
        request_body=EmployeeSerializer,
        operation_summary="Edit employee info",
        operation_description="This allows a company to edit the info of one of it's employees",
        tags=["Employee Endpoints"],
    )
    def patch(self, request, pk):

        """
        Edit employee info
        :param request:
        :param pk: employee_id
        :return: Employee | ValidationError
        """

        employee = self.get_employee_by_id_or_404(pk)
        companies = self.check_if_logged_as_company(request)
        company = self.check_if_employee_part_of_company(employee, companies)
        if company:
            data = {**request.data, 'company_id': company.id}
            serializer = EmployeeSerializer(employee, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete employee",
        operation_description="This allows a company to delete one of it's employees",
        tags=["Employee Endpoints"],
    )
    def delete(self, request, pk):

        """
        Delete employee info
        :param request:
        :param pk: employee_id
        :return: Http204 | ValidationError
        """

        employee = self.get_employee_by_id_or_404(pk)
        companies = self.check_if_logged_as_company(request)
        if self.check_if_employee_part_of_company(employee, companies):
            employee.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)