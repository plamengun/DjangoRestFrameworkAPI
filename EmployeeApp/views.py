from django.http import JsonResponse
from django.http import Http404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from accounts.serializers import UserSerializer
from EmployeeApp.serializers import CompaniesSerializer
from EmployeeApp.models import Companies, User


def api_home(request, *args, **kwargs):
    return JsonResponse({"message": 'Hi there, this is a Django API response serving as a homepage :D'})


class CompaniesList(APIView):
    def get(self, request):
        companies = Companies.objects.all()
        serializer = CompaniesSerializer(companies, many=True)
        return Response(serializer.data)


class CompanyCreate(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        company_name_exists = Companies.objects.filter(company_name=request.data['company_name']).exists()
        if company_name_exists:
            raise ValidationError("Company with the same name already exists")

        user_id = Token.objects.get(key=request.auth.key).user_id
        user = User.objects.get(id=user_id)
        user_info= UserSerializer(instance=user)
        print(user_info)
        # user = request.user
        u = {'email': user_info.data['email'], 'password': user_info.data['password']}
        # user = {'email': request.data['email'], 'password': request.data['password']}
        serializer = CompaniesSerializer(data={'user':user_id, 'company_name':request.data['company_name'], 'company_description':request.data['company_description'], 'company_logo':request.data['company_logo']})
        # serializer = CompaniesSerializer(data=request.data)
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
        serializer = CompaniesSerializer(company)
        return Response(serializer.data)

    def put(self, request, pk):
        company = self.get_company_by_id_or_404(pk)
        serializer = CompaniesSerializer(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        company = self.get_company_by_id_or_404(pk)
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

