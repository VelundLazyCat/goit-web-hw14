from unittest.mock import Mock, MagicMock
from conftest import TestingSessionLocal
from models import User
import pytest
from sqlalchemy import select


user_data = {"username": "agent007",
             "email": "agent007@gmail.com", "password": "12345678"}


def test_create_user(client, monkeypatch):
    mock_send_email = Mock()
    monkeypatch.setattr("auth_routes.send_email", mock_send_email)
    response = client.post("api/auth/signup", json=user_data)

    assert response.status_code == 201, response.text
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert "password" not in data


def test_repeat_create_user(client, monkeypatch):
    mock_send_email = Mock()
    monkeypatch.setattr("auth_routes.send_email", mock_send_email)
    response = client.post("api/auth/signup", json=user_data)

    assert response.status_code == 409, response.text
    data = response.json()
    assert data["detail"] == "Account already exists"


def test_login_user_not_confirmed(client):
    response = client.post("api/auth/login",
                           data={"username": user_data.get('email'), "password": user_data.get('password')})
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Email not confirmed"


@pytest.mark.asyncio
async def test_login_user(client):
    async with TestingSessionLocal() as session:
        current_user = await session.execute(select(User).where(User.email == user_data.get("email")))
        current_user = current_user.scalar_one_or_none()
        if current_user:
            current_user.confirmed = True
            await session.commit()

    response = client.post("api/auth/login",
                           data={"username": user_data.get("email"), "password": user_data.get("password")})
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert "token_type" in data


def test_login_wrong_password(client):
    response = client.post("api/auth/login",
                           data={"username": user_data.get("email"), "password": "password"})
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Invalid password"


def test_login_wrong_email(client):
    response = client.post("api/auth/login",
                           data={"username": "email", "password": user_data.get("password")})
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Invalid email"
