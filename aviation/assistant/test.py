import pytest
from django.urls import reverse
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_nl_query_returns_suggestion():
    client = APIClient()
    url = reverse("nl-query")

    resp = client.post(url, {"prompt": "Show flights from Lviv to Krakow tomorrow"}, format="json")

    assert resp.status_code == 200

    assert "suggestion" in resp.data, f"Response missing suggestion: {resp.data}"
    assert isinstance(resp.data["suggestion"], str)
    assert len(resp.data["suggestion"]) > 0