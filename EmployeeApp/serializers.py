from rest_framework import serializers
from .models import Companies, Employees
from accounts.serializers import SignUpSerializer, UserSerializer
from accounts.models import User


class CompaniesSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Companies
        fields = ('user_id', 'company_name', 'company_description', 'company_logo')

    def create(self, validated_data):
        company, is_created = Companies.objects.get_or_create(
                                        company_name=validated_data['company_name'],
                                        company_description=validated_data['company_description'],
                                        company_logo=validated_data['company_logo'],
                                        user_id=validated_data['user_id'],
                                        )
        return company


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = ('id', 'first_name', 'last_name', 'date_of_birth', 'photo', 'position', 'salary')

    def set_company(self, company):
        self.company = company

    def create_obj(self, validated_data):
        
        employee = Employees.objects.create(id=validated_data['id'],
                                            first_name=validated_data['first_name'],
                                            last_name=validated_data['last_name'],
                                            date_of_birth=validated_data['date_of_birth'],
                                            photo=validated_data['photo'],
                                            position=validated_data['position'],
                                            salary=validated_data['salary'],
                                            company=self.company,
                                            )

        employee.save()
        return employee