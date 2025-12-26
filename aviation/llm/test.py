import pytest
from django.urls import reverse
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_nl_query_empty_prompt():
    client = APIClient()
    url = reverse("nl-query")
    resp = client.post(url, {"prompt": ""}, format="json")
    assert resp.status_code == 400
    assert resp.data["status"] == "error"

@pytest.mark.django_db
def test_nl_query_unknown_intent():
    client = APIClient()
    url = reverse("nl-query")
    resp = client.post(url, {"prompt": "Some random text"}, format="json")
    assert resp.status_code == 200
    assert resp.data["status"] in ["error", "ok"]