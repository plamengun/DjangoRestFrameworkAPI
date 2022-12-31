import pytest
from rest_framework.test import APIClient


client = APIClient()
MOCK_COMPANY_RESPONSE = {'company_name': 'Test Company',
                         'company_description': 'comp descr',
                         'company_logo': 'logo.asd'}



@pytest.mark.django_db
def test_get_company_list_view(register_and_login_user):
    token = register_and_login_user.data['token']

    client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    data = {'company_name': 'Test Company',
            'company_description': 'comp descr',
            'company_logo': 'logo.asd'
            }
    client.post('/api/companies', data=data, format='json')
    request = client.get('/api/companies/', format='json')
    assert len(request.data) == 1
    assert request.status_code == 200


@pytest.mark.django_db
def test_company_create(register_and_login_user):
    token = register_and_login_user.data['token']

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


# @pytest.mark.django_db
# def test_get_own_company_info_successful(register_and_login_user):
#     token = register_and_login_user.data['token']
#
#     client.credentials(HTTP_AUTHORIZATION='Token ' + token)
#
#     data = {'company_name': 'Test Company',
#             'company_description': 'comp descr',
#             'company_logo': 'logo.asd'
#             }
#     client.post('/api/companies', data=data, format='json')
#
#     request = client.get('/api/companies/1/', format='json')
#
#     assert request.data == MOCK_COMPANY_RESPONSE


@pytest.mark.django_db
def test_get_own_company_info_successful(register_and_login_user, create_company):
    token = register_and_login_user.data['token']

    client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    comp = create_company

    request = client.get('/api/companies/1/', format='json')

    assert request.data == MOCK_COMPANY_RESPONSE
