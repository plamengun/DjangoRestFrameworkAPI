import pytest
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db
def test_signup_view():
    payload = {
        "username": "Plamen",
        "email": "plamenmgunchev@gmail.com",
        "password": "12345678"
    }

    response = client.post("/api/auth/signup/", payload)

    assert response.data["message"] == "User Created Successfully"