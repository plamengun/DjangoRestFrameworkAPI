from django.http import JsonResponse
from django.http import Http404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.permissions import IsAuthenticated

from EmployeeApp.serializers import CompanySerializer, EmployeeSerializer
from EmployeeApp.models import Companies


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