import pytest
from rest_framework.test import APIClient
from rest_framework.serializers import ErrorDetail

client = APIClient()
MOCK_USER = {'email': 'plamenmgunchev@gmail.com', 'username': 'Plamen'}


@pytest.mark.django_db
def test_signup_view_post_when_successful():
    payload = {
        "username": "Plamen",
        "email": "plamenmgunchev@gmail.com",
        "password": "12345678"
    }

    response = client.post("/api/auth/signup", payload)

    assert response.data["message"] == "User Created Successfully"
    assert response.data["data"] == MOCK_USER


@pytest.mark.django_db
def test_signup_view_post_when_unsuccessful():
    payload = {}

    response = client.post("/api/auth/signup", payload)

    assert response.data['email'] == [ErrorDetail(string='This field is required.',
                                                  code='required')]
    assert response.data['password'] == [ErrorDetail(string='This field is required.',
                                                     code='required')]
    assert response.data['username'] == [ErrorDetail(string='This field is required.',
                                                     code='required')]


@pytest.mark.django_db
def test_login_view_post_when_successful():
    payload = {
        "username": "Plamen",
        "email": "plamenmgunchev@gmail.com",
        "password": "12345678"
    }

    client.post("/api/auth/signup", payload)

    response = client.post("/api/auth/login", {"email": "plamenmgunchev@gmail.com",
                                               "password": "12345678"})

    assert response.data["message"] == "Login Successful"
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_view_post_when_unsuccessful():
    payload = {
        "username": "Plamen",
        "email": "plamenmgunchev@gmail.com",
        "password": "12345678"
    }

    client.post("/api/auth/signup", payload)

    response = client.post("/api/auth/login", {"email": "plamenmgunchev@gmail.com",
                                               "password": "1"})

    assert response.data["message"] == "Invalid username or password"
    assert response.status_code == 401

#ToDo Test when user is not logged - should return AnonymousUser code 200
@pytest.mark.django_db
def test_get_logged_in_user_view():
    payload = {
        "username": "Plamen",
        "email": "plamenmgunchev@gmail.com",
        "password": "12345678"
    }
    client.post("/api/auth/signup", payload)
    login_response = client.post("/api/auth/login", {"email": "plamenmgunchev@gmail.com",
                                                     "password": "12345678"})
    token = login_response.data['token']

    cred = client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    response = client.get("/api/auth/login", data=cred)

    assert response.data["user"] == 'Plamen'
    assert response.data["auth"] == token
    assert response.status_code == 200
