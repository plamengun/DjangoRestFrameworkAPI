import pytest
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient
from accounts.models import User

from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from EmployeeApp.models import Companies


client = APIClient()


@pytest.mark.django_db
def test_company_create():
    # # Create a client and log in as a user
    # factory = APIRequestFactory()
    # user = User.objects.create_user(username='testuser', email="test@gmail.com",
    #                                 password='testpass')
    # get_user = User.objects.get(username='testuser')
    # view = CompanyCreate.as_view()
    #
    # # Create a company
    # data = {'company_name': 'Test Company',
    #         'company_description': 'comp descr',
    #         'company_logo': 'logo.asd'
    #         }
    # request = factory.post('/api/companies', data=data, format='json')
    # force_authenticate(request, user=get_user)
    # response = view(request)
    # assert User.objects.count() == 1


    user = get_user_model()
    our_user = user.objects.create(username="testuser", password="asb", email="email@mail.com")
    token = Token.objects.create(user=our_user)
    print(token.key, "token")
    print(our_user.id)
    client.credentials(HTTP_AUTHORIZATION="Token" + token.key)

    data = {'company_name': 'Test Company',
            'company_description': 'comp descr',
            'company_logo': 'logo.asd'
            }
    request = client.post('/api/companies', data=data, format='json')

    assert request.data == 'asd'

    # # Check that the company was created in the database
    # company = Companies.objects.get(company_name='Test Company')
    # assert company.user_id == user.id
    #
    # # Try to create a company with the same name
    # data = {'company_name': 'Test Company'}
    # response = client.post('/api/companies', data=data, format='json')
    # assert response.status_code == 400
    #
    # # Check that the company was not created in the database
    # assert Companies.objects.filter(company_name='Test Company').count() == 1


# @pytest.mark.django_db
# def test_company_view_comapnies_list():
#     factory = APIRequestFactory()
#     data = {'company_name': 'Test Company',
#             'company_description': 'comp descr',
#             'company_logo': 'logo.asd',
#             'user_id': 1
#             }
#     response = factory.post('/api/companies', data)
#
#     assert Companies.objects.count() == 1