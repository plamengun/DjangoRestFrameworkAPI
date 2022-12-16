from django.urls import path

from EmployeeApp.views import CompaniesList, CompanyCreate, CompanyDetails, EmployeeCreate, EmployeesList, EmployeeDetails

#ToDo fix urls
urlpatterns = [
    path('companies/', CompaniesList.as_view(), name="companies_view"),
    path('companies', CompanyCreate.as_view(), name="company_create"),
    path('companies/<int:pk>/', CompanyDetails.as_view(), name="company_get_by_id"),
    path('employees', EmployeeCreate.as_view(), name="employee_create"),
    path('employees/', EmployeesList.as_view(), name="employees_view"),
    path('employees/<int:pk>/', EmployeeDetails.as_view(), name="employee_get_by_id"),
    ]