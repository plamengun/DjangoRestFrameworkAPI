from rest_framework import serializers
from .models import Companies, Employees


class CompanySerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    id = serializers.ReadOnlyField()

    class Meta:
        model = Companies
        fields = ('id', 'user_id', 'company_name', 'company_description', 'company_logo')

    def create(self, validated_data):
        company, is_created = Companies.objects.get_or_create(
            company_name=validated_data['company_name'],
            company_description=validated_data['company_description'],
            company_logo=validated_data['company_logo'],
            user_id=validated_data['user_id'],
        )
        return company


class EmployeeSerializer(serializers.ModelSerializer):
    company_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Employees
        fields = ('company_id', 'first_name', 'last_name',
                  'date_of_birth', 'photo', 'position', 'salary')

    def create(self, validated_data):
        employee, is_created = Employees.objects.get_or_create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            date_of_birth=validated_data['date_of_birth'],
            photo=validated_data['photo'],
            position=validated_data['position'],
            salary=validated_data['salary'],
            company_id=validated_data['company_id'],
        )
        return employee
