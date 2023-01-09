import pytest
from fastapi import status, HTTPException
from src import schemas
from jose import jwt
from src.config import settings
from src.oauth2 import verify_access_token
# from tests.conftest import test_user

def test_checkSession_failed(client):
    res = client.get("/api/users/checkSession/")
    failed_response = res.json()
    assert failed_response['detail'] == 'Not authenticated'
    assert res.status_code == 401

def test_checkSession_success(authorized_client):
    credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate" : "Bearer"}
    )

    res = authorized_client.get("/api/users/checkSession/")
    res_json = res.json()

    access_token = res_json['token']
    token_type = res_json['token_type']

    verified = verify_access_token(access_token, credentials_exception)

    assert res.status_code == 200
    assert token_type == 'bearer'



@pytest.mark.parametrize("username, email, password, status_code", [
    (
        "testy", "testy@gmail.com", "password123", 201
    ),
    (
        "testy2", "testy2@gmail.com", "password123", 201
    ),
    (
        "testy3", "testy3@gmail.com", "password123", 201
    ),
])
def test_registration_success(client, username, email, password, status_code):
    res = client.post('/api/users/register', json={
        "username" : username,
        "email" : email,
        "password" : password
    })
    res_json = res.json()
    assert res.status_code == status_code
    assert username == res_json['username']
    assert email == res_json['email']


def test_registration_fail(client):
    res = client.post('/api/users/register', json={
        "username" : "somebad",
        "email" : "bademail",
        "password" : "password123"
    })
    
    res_json = res.json()
    
    assert res.status_code == 422


def test_login_success(client, test_user: schemas.UserOut):
    res = client.post("/api/users/login", json={
        "email" : test_user['email'],
        "password" : test_user['password']
    })
    # res_json = await res.json()


    login_res = schemas.Token(**res.json())

    payload = jwt.decode(login_res.token, settings.secret_key, algorithms=[settings.algorithm])

    id = payload.get('user_id')

    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

def test_login_fail_password(client, test_user: schemas.UserOut):
    res = client.post("/api/users/login", json={
        "email" : test_user['email'],
        "password" : "badpassword"
    })

    res_json = res.json()
    assert res_json['detail'] == 'Invalid Credentials'
    assert res.status_code == 403

def test_login_fail_email(client, test_user: schemas.UserOut):
    res = client.post("/api/users/login", json={
        "email" : 'bademail@gmail.com',
        "password" : test_user['password']
    })

    res_json = res.json()
    assert res_json['detail'] == 'Invalid Credentials'
    assert res.status_code == 403

def test_update_user_username_successful(authorized_client, test_user: schemas.UserOut):
    res = authorized_client.put(f"/api/users/{test_user['id']}", json={
        "username" : 'testme'
    })
    res_json = res.json()
    assert res_json['id'] == test_user['id']
    assert res_json['username'] == 'testme'

def test_update_user_email_successful(authorized_client, test_user: schemas.UserOut):
    res = authorized_client.put(f"/api/users/{test_user['id']}", json={
        "email" : 'test_update@gmail.com'
    })
    res_json = res.json()

    assert res_json['id'] == test_user['id']
    assert res_json['email'] == 'test_update@gmail.com'