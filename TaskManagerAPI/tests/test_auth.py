import pytest
from src.main import app

def test_register_success(client):
    response = client.post(
        "/api/auth/register",
        json={"email": "new@example.com", "password": "StrongPass1", "full_name": "New User"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "new@example.com"
    assert "id" in data

def test_register_duplicate_email(client, test_user):
    response = client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "StrongPass1"}
    )
    assert response.status_code == 400
    assert "already registered" in response.text

def test_login_success(client, test_user):
    response = client.post(
        "/api/auth/login",
        data={"username": "test@example.com", "password": "TestPass123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_password(client, test_user):
    response = client.post(
        "/api/auth/login",
        data={"username": "test@example.com", "password": "wrong"}
    )
    assert response.status_code == 401