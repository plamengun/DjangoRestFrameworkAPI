from django.urls import path

from employee_app.views import CompaniesList, CompanyCreate, CompanyDetails, EmployeeCreate, \
    EmployeesList, EmployeeDetails

#ToDO URL must be uniqie regardless of the request method used :?
urlpatterns = [
    path('companies/', CompaniesList.as_view(), name="companies_view"),
    path('companies', CompanyCreate.as_view(), name="company_create"),
    path('companies/<int:pk>/', CompanyDetails.as_view(), name="company_get_by_id"),
    path('<int:pk>/employees/', EmployeeCreate.as_view(), name="employee_create"),
    path('<int:pk>/employees', EmployeesList.as_view(), name="employees_view"),
    path('employees/<int:pk>', EmployeeDetails.as_view(), name="employee_get_by_id"),
    ]