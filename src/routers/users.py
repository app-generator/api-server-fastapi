from fastapi import status, HTTPException, Depends, APIRouter, Request
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session
from typing import List

import src.schemas as schemas
import src.models as models
import src.oauth2 as oauth2
from src.helpers.database import get_db
from src.helpers.utils import hash, verify
from src.config import settings

from jose import JWTError
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

import requests


router = APIRouter(
    prefix = "/api/users",
    tags = ['Users']
)


# @router.get('/', response_model=List[schemas.UserOut])
# async def get_users(db: Session = Depends(get_db)):
#     users = db.query(models.User).all()

#     if not users:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Was Not Found')

#     return users

# @router.get('/{id}', response_model=schemas.UserOut)
# async def get_user(id: int, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id).first()

#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Was Not Found')

#     return user


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_passord = hash(user.password)
    user.password  = hashed_passord

    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# @router.post('/login', response_model=schemas.Token)
@router.post('/login')
# async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
async def login(request: Request, db: Session = Depends(get_db)):
    
    json_request = await request.json()

    user_credentials = schemas.UserLogin(email=json_request.get('email'), password=json_request.get('password'))
    
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')

    access_token = oauth2.create_access_token(data = {"user_id" : user.id})

    return {
        "token" : access_token,
        "token_type" : "bearer"
    }
    # return {
    #     "access_token" : access_token,
    #     "token_type" : "bearer"
    # }


@router.put('/{id}', response_model=schemas.UserOut)
async def update_user(id: int, updated_user: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):

    user_query = db.query(models.User).filter(models.User.id == id)
   
    user = user_query.first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Was Not Found')


    if current_user.id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform requested action')

    if (not updated_user.username):
        updated_user.username = current_user.username

    if (not updated_user.password):
        updated_user.password = current_user.password
    else:
        hashed_passord = hash(updated_user.password)
        updated_user.password  = hashed_passord

    if (not updated_user.email):
        updated_user.email = current_user.email


    user_query.update(updated_user.dict(), synchronize_session=False)

    db.commit()

    return user_query.first()

@router.get('/checkSession', response_model=schemas.Token, status_code=status.HTTP_200_OK)
async def check_session(request: Request, current_user: int = Depends(oauth2.get_current_user)):
    credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate" : "Bearer"}
    )

    bearer_token = request.headers.get('authorization')

    if (bearer_token):
        token_type, token = bearer_token.split(' ')
        verified = oauth2.verify_access_token(token, credentials_exception)
        return {
            "token" : token,
            "token_type" : 'bearer'
        }
    
    raise JWTError


@router.get("/github_login")
async def github_login(request: Request):
    if not settings.github_is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing a Required Github Credential, check your environment variables")

    github_login_url = f'https://github.com/login/oauth/authorize?client_id={settings.github_client_id}'
    redirect = RedirectResponse(url=github_login_url)
    redirect.status_code = 302
    return redirect


@router.get("/github_auth")
async def authorize_github(request: Request):
    authorization_code = request.query_params.get('code')
    try:        
        url = f'https://github.com/login/oauth/access_token?client_id={settings.github_client_id}&client_secret={settings.github_secret_key}&code={authorization_code}'
        headers = {
            'accept': 'application/json'
        }
        res = requests.post(url, headers=headers)

        data = res.json()

        access_token = data.get('access_token')

        access_token = 'token ' + access_token
        url = 'https://api.github.com/user'
        headers = {"Authorization": access_token}
        resp = requests.get(url=url, headers=headers)
        userData = resp.json()
        return userData
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization Code")


@router.post('/logout', status_code=status.HTTP_200_OK)
async def logout(request: Request, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
        
    invalid_token = request.headers.get('authorization')

    new_blocked_token = schemas.blockedTokenCreate(jwt_token=invalid_token)

    new_blocked_token_model = models.JWTTokenBlocklist(**new_blocked_token.dict())

    db.add(new_blocked_token_model)
    db.commit()

    return {'success' : True}
