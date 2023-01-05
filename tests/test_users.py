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


    access_token = res_json['access_token']
    token_type = res_json['token_type']

    verified = verify_access_token(access_token, credentials_exception)

    assert res.status_code == 200
    assert token_type == 'bearer'

    
def test_registration_success(client):
    res = client.post('/api/users/register', json={
        "username" : "Testy",
        "email" : "testy@gmail.com",
        "password" : "password123"
    })

    res_json = res.json()

    assert res.status_code == 201
    print (res_json)
    # print (res.status_code)
    # print('\n\n')

    