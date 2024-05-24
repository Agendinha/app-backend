import pytest
from fastapi.testclient import TestClient
from app.main import app, pwd_context, create_access_token, verify_password
from app.model import UserBase, UserLogin

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_user_dao(mocker):
    mocker.patch('app.dao.UserDAO.insert')
    mocker.patch('app.dao.UserDAO.get_password', return_value=None)

def test_register_user():
    user = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123",
        "phone": "1234567890",
        "postalcode": "12345",
        "usertype": "user"
    }
    response = client.post("/api/v1/register/", json=user)
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}


def test_verify_password_correct():
    # Senha correta
    hashed_password = pwd_context.hash("password123")
    assert verify_password("password123", hashed_password) == True

def test_verify_password_incorrect():
    # Senha incorreta
    hashed_password = pwd_context.hash("password123")
    assert verify_password("wrongpassword", hashed_password) == False

def test_create_access_token_returns_string():
    # Testando se o token é uma string
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    assert isinstance(token, str)

def test_create_access_token_has_jwt_format():
    # Testando se o token tem o formato JWT
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    assert len(token.split(".")) == 3