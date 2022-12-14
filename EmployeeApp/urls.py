from django.urls import path

from EmployeeApp.views import CompaniesList, CompanyCreate, CompanyDetails

#ToDo fix urls
urlpatterns = [
    path('companies/', CompaniesList.as_view(), name="companies_view"),
    path('companies', CompanyCreate.as_view(), name="companies_create"),
    path('companies/<int:pk>/', CompanyDetails.as_view(), name="company_get_by_id"),
    ]