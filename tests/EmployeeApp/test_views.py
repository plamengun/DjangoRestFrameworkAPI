import pytest
from rest_framework.test import APIClient


client = APIClient()


@pytest.mark.django_db
def test_signup_view():
    payload = {
        "company_name": "comp13",
        "company_description": "comp descr",
        "company_logo": "logo.asd"
    }

    response = client.post("/api/companies", payload)
    data = response.data

    assert response.data["detail"] == payload