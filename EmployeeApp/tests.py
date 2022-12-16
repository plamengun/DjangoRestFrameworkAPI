from rest_framework.test import APITestCase, APIRequestFactory
from .views import CompaniesList, CompanyCreate
from django.urls import reverse


class CompanyListCreateTestCase(APITestCase):
    
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = CompaniesList.as_view()
        self.url = reverse("companies_view")
        

    def test_list_companies(self):
        
        request = self.factory.get(self.url)
        response = self.view(request)

        self.assertEqual(response.status_code, 200)

    def test_company_creation(self):
        pass