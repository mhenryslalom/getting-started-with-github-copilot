import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_and_unregister():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Unregister first in case already present
    client.post(f"/activities/{activity}/unregister?email={email}")
    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    # Try duplicate sign up
    response_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert response_dup.status_code == 400
    # Unregister
    response_unreg = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response_unreg.status_code == 200
    assert "Successfully unregistered" in response_unreg.json()["message"]
    # Try duplicate unregister
    response_unreg_dup = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response_unreg_dup.status_code == 400
