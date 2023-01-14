import pytest
from rest_framework.test import APIClient

client = APIClient()
#ToDO Look into solving the code repetition with company creation in the tests
MOCK_COMPANY_DATA = {'company_name': 'Test Company',
                     'company_description': 'comp descr',
                     'company_logo': 'logo.asd'}


@pytest.mark.django_db
def test_get_company_list_view(register_and_login_user):
    token = register_and_login_user.data['token']

    client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    data = MOCK_COMPANY_DATA
    client.post('/api/companies', data=data, format='json')
    request = client.get('/api/companies/', format='json')
    assert len(request.data) == 1
    assert request.status_code == 200


@pytest.mark.django_db
def test_company_create(register_and_login_user):
    token = register_and_login_user.data['token']

    client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    data = MOCK_COMPANY_DATA
    request = client.post('/api/companies', data=data, format='json')

    assert request.data['company_name'] == MOCK_COMPANY_DATA['company_name']
    assert request.status_code == 201


@pytest.mark.django_db
def test_get_own_company_info_successful(register_and_login_user):
    token = register_and_login_user.data['token']
    client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    data = MOCK_COMPANY_DATA
    request_create = client.post('/api/companies', data=data, format='json')

    request = client.get(f"/api/companies/{request_create.data['id']}/", format='json')

    assert request.data['company_name'] == MOCK_COMPANY_DATA['company_name']
    assert request.status_code == 200


@pytest.mark.django_db
def test_patch_own_company_info_successful(register_and_login_user):
    token = register_and_login_user.data['token']
    client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    data = MOCK_COMPANY_DATA
    request_create = client.post('/api/companies', data=data, format='json')
    payload = dict(company_name='Updated_name')

    request = client.patch(f"/api/companies/{request_create.data['id']}/", payload)

    assert request.data['company_name'] == 'Updated_name'
    assert request.status_code == 200


@pytest.mark.django_db
def test_delete_own_company_successful(register_and_login_user):
    token = register_and_login_user.data['token']
    client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    data = MOCK_COMPANY_DATA
    request_create = client.post('/api/companies', data=data, format='json')

    request = client.delete(f"/api/companies/{request_create.data['id']}/", format='json')

    assert request.status_code == 204
