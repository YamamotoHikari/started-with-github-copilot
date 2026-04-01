import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# --- Activities List ---
def test_get_activities():
    # Arrange
    # (No special setup needed)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

# --- Signup Success ---
def test_signup_success():
    # Arrange
    test_email = "testuser1@mergington.edu"
    activity = "Math Olympiad"
    # Ensure not already signed up
    client.delete(f"/activities/{activity}/unregister", params={"email": test_email})

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": test_email})

    # Assert
    assert response.status_code == 200
    assert f"Signed up {test_email}" in response.json()["message"]

# --- Signup Duplicate ---
def test_signup_duplicate():
    # Arrange
    test_email = "testuser2@mergington.edu"
    activity = "Science Club"
    # 1回目登録
    client.delete(f"/activities/{activity}/unregister", params={"email": test_email})
    client.post(f"/activities/{activity}/signup", params={"email": test_email})

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": test_email})

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

# --- Unregister Success ---
def test_unregister_success():
    # Arrange
    test_email = "testuser3@mergington.edu"
    activity = "Art Workshop"
    # 事前に登録
    client.post(f"/activities/{activity}/signup", params={"email": test_email})

    # Act
    response = client.delete(f"/activities/{activity}/unregister", params={"email": test_email})

    # Assert
    assert response.status_code == 200
    assert f"Removed {test_email}" in response.json()["message"]

# --- Unregister Not Registered ---
def test_unregister_not_registered():
    # Arrange
    test_email = "notregistered@mergington.edu"
    activity = "Basketball Club"
    # 念のため削除
    client.delete(f"/activities/{activity}/unregister", params={"email": test_email})

    # Act
    response = client.delete(f"/activities/{activity}/unregister", params={"email": test_email})

    # Assert
    assert response.status_code == 404
    assert "not registered" in response.json()["detail"]
