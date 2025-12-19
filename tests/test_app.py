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

def test_signup_and_unregister():
    # Test signup
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_resp.status_code == 200
    assert f"Signed up {email}" in signup_resp.json()["message"]

    # Test duplicate signup
    dup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert dup_resp.status_code == 400
    assert "already signed up" in dup_resp.json()["detail"]

    # Test unregister
    unreg_resp = client.post(f"/activities/{activity}/unregister?email={email}")
    assert unreg_resp.status_code == 200
    assert f"{email} a été désinscrit" in unreg_resp.json()["message"]

    # Test unregister not registered
    unreg_resp2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert unreg_resp2.status_code == 400
    assert "not registered" in unreg_resp2.json()["detail"]
