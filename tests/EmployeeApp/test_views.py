import pytest
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db
def test_company_create():
    payload = {
        "username": "testuser",
        "email": "email@mail.com",
        "password": "12345678"
    }

    client.post("/api/auth/signup", payload)
    login_response = client.post("/api/auth/login", {"email": "email@mail.com",
                                                     "password": "12345678"})
    token = login_response.data['token']

    client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    data = {'company_name': 'Test Company',
            'company_description': 'comp descr',
            'company_logo': 'logo.asd'
            }
    request = client.post('/api/companies', data=data, format='json')

    assert request.data == {'company_name': 'Test Company',
                            'company_description': 'comp descr',
                            'company_logo': 'logo.asd'}
    assert request.status_code == 201
