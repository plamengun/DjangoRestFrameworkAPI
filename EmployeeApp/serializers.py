from rest_framework import serializers
from .models import Companies, Employees


class CompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Companies
        fields = ('id', 'company_name', 'company_description', 'company_logo')

    def create_obj(self, validated_data):

        company = Companies.objects.create(id=validated_data['id'],
                                        company_name=validated_data['company_name'],
                                        company_description=validated_data['company_description'],
                                        company_logo=validated_data['company_logo'],
                                        )

        company.save()
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